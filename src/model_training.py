from datetime import datetime
from math import e
from pathlib import Path
from typing import Mapping
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config.base_config import Config, get_config
from config.model_params import LightGPMParams, RandomSearchParams
from config.paths import Paths
from src.logger import get_logger
from src.utils.common import DataSplitter, load_data
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining(DataSplitter):
    config: Config
    paths: Paths
    params_dist: LightGPMParams
    random_search_params: RandomSearchParams

    def __init__(self) -> None:
        self.config = get_config()
        self.paths = self.config.paths
        self.params_dist = self.config.model.light_params
        self.random_search_params = self.config.model.random_search

    def load_data(self, csv_path: Path) -> pd.DataFrame:
        logger.info(f"Loading data from {csv_path}")
        df = load_data(csv_path)
        logger.info(f"{csv_path} loaded")
        return df

    def load_and_split_data(self) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        logger.info("Starting load_and_split process")
        train_df = self.load_data(self.paths.processed_training_data_filepath)
        X_train, y_train = self._split_df_by_booking_status(train_df)

        test_df = self.load_data(self.paths.processed_test_data_filepath)
        X_test, y_test = self._split_df_by_booking_status(test_df)
        
        assert train_df.columns.equals(test_df.columns)

        logger.info("Data has been loaded and split")

        return X_train, y_train, X_test, y_test
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series):
        logger.info("Setting Up model classifier")

        model = lgb.LGBMClassifier(random_state=self.config.random_state)

        logger.info("Setting up hyperparameter tuning")
        random_search = RandomizedSearchCV(
            **self.random_search_params.model_dump(mode="json"),
            param_distributions=self.params_dist.model_dump(mode="json"),
            estimator=model,
            )
        
        logger.info("Starting hyperparameter tuning; this takes 10-20 minutes if you don't have a graphics card")
        random_search.fit(X_train, y_train)
        logger.info("Finished tuning hyperparameters")

        best_params = random_search.best_params_
        best_lgbm_model = random_search.best_estimator_

        logger.info(f"Best params: {best_params}")
        return best_lgbm_model
    
    def evaluate_model(self, model, X_test, y_test) -> dict[str, float]:
        y_predict = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_predict)
        precision = precision_score(y_test, y_predict)
        recall = recall_score(y_test, y_predict)
        f1 = f1_score(y_test, y_predict)

        result = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,  
        }
        logger.info(result)

        return result
                
    def save(self, model):
        logger.info("Saving the model")
        joblib.dump(model, self.paths.model_output_filepath)
        logger.info(f"Finished saving model to {self.paths.model_output_filepath}")

    def run(self) -> Mapping[str, float]:
        logger.info("Begin training model")
        start = datetime.now()

        try:
            with mlflow.start_run():
                logger.info("Starting mlflow experimentation")
                logger.info("Logging the training and testing datasets to mlflow")
                mlflow.log_artifact(self.paths.processed_training_data_filepath, artifact_path="datasets")
                mlflow.log_artifact(self.paths.processed_test_data_filepath, artifact_path="datasets")

                X_train, y_train, X_test, y_test = self.load_and_split_data()
                model = self.train_model(X_train, y_train)

                metrics = self.evaluate_model(model, X_test, y_test)

                mlflow.log_params(model.get_params())
                mlflow.log_metrics(metrics)

                self.save(model)

                logger.info("Logging the model into mlflow")
                mlflow.log_artifact(self.paths.model_output_filepath)
        except Exception as e:
            logger.exception("Failed to train model", e)
        finally:
            # Record the timing even if we've failed
            end = datetime.now()
            msg = f"Training took {(end - start).seconds / 60} minutes"
            logger.info(msg)
            print(msg)

        logger.info("Finished training model")
        return metrics



if "__main__" == __name__:
    train = ModelTraining()
    train.run() 

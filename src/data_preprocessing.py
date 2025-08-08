from pathlib import Path
import pandas as pd
import numpy as np
from config.base_config import Config, get_config
from src.logger import get_logger
from src.utils.common import DataSplitter, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor(DataSplitter):
    train_path: Path
    test_path: Path
    processed_dir: Path
    config: Config

    _random_state: int = 42

    def __init__(self, config: Path = Path(__file__).parent.parent / "config" / "config") -> None:
        self.config = get_config()

    def _encode_categories(self, df: pd.DataFrame, cat_cols: list[str]) -> dict:
        """
        For each category column, create an encoder to make the data
        ingestable by the model.

        Apply the encoder to those columns.

        Returns a dict containing the original key:encoded value

        TODO: Fix Pylance error: https://stackoverflow.com/a/58868765
        """
        le = LabelEncoder()
        mappings = {}

        for col in cat_cols:
            # apply the encoding, ensuring the starting data 
            # contains only strings
            df[col] = le.fit_transform(df[col])

            # create a mapping of the original key: encoded value
            # the int is because otherwise we get pandas type np.int64(), hard to read
            mappings[col] = {k:v for k,v in zip(le.classes_, [int(x) for x in le.transform(le.classes_)])}

            logger.info(f"Data Mappings for {col}: {mappings[col]}")

        return mappings
    
    def _adjust_skew(self, df: pd.DataFrame) -> None:
        """
        Reduce skew in place
        """
        logger.info("Adjusting skew")

        sk = df.skew()

        for col in df.columns:
            if sk[col] > self.config.data_processing.skewness_threshold:
                df[col] = np.log1p(df[col])
        logger.info("Finished adjusting skew")


    def adjust_imbalance(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Ajdusting imbalance (overfit)")
        X, y = self._split_df_by_booking_status(df)

        smote = SMOTE(random_state=self._random_state)
        X_res, y_res = smote.fit_resample(X, y)

        balanced = pd.DataFrame(X_res, columns=X.columns)
        balanced["booking_status"] = y_res

        logger.info("Finished adjusting imbalance")

        return balanced
    
    def select_top_features(self, df: pd.DataFrame):
        logger.info(f"Selecting top {self.config.data_processing.number_of_features} features")
        X, y = self._split_df_by_booking_status(df)

        model = RandomForestClassifier(random_state=self._random_state)
        model.fit(X, y)
        feature_importance = model.feature_importances_
        feature_df = pd.DataFrame({
            "feature": X.columns,
            "importance": feature_importance
        })
        top_features_df = feature_df.sort_values(by="importance", ascending=False)
        top_ten = top_features_df["feature"].head(self.config.data_processing.number_of_features).values
        top_x_df = df[top_ten.tolist() + ["booking_status"]]

        logger.info("Finished selecting top features")
        logger.info(f"Top features: {top_ten}")

        return top_x_df


    def preprocess_data(self, df: pd.DataFrame):
        logger.info("Beginning data preprocessing")

        # Get rid of the columns we don't care about
        df.drop(columns=["Unnamed: 0", "Booking_ID"], inplace=True)

        # Get rid of any duplicated data
        df.drop_duplicates(inplace=True)

        # Split the columns up by whether they're a categor or number
        self._encode_categories(df, self.config.data_processing.categorical_columns)
        self._adjust_skew(df)
        return df

    def save(self, df: pd.DataFrame, location: Path):
        logger.info("Saving preprocessed data")

        df.to_csv(location, index=False)

        logger.info("Finished saving preprocessed data")

    def run(self):
        logger.info("Beginning data processing")
        train_df = load_data(self.config.paths.train_filepath)
        test_df = load_data(self.config.paths.test_filepath)

        preprocessed_train_df = self.preprocess_data(train_df)
        preprocessed_test_df = self.preprocess_data(test_df)

        balanced_train_df = self.adjust_imbalance(preprocessed_train_df)
        balanced_test_df = self.adjust_imbalance(preprocessed_test_df)

        top_features_train_df = self.select_top_features(balanced_train_df)
        # Ensure the top columns are the same
        top_features_test_df = balanced_test_df[top_features_train_df.columns]

        self.save(top_features_train_df, self.config.paths.processed_training_data_filepath)
        self.save(top_features_test_df, self.config.paths.processed_test_data_filepath)

        logger.info("Finished processing data")


if "__main__" == __name__:
    processor = DataProcessor()
    processor.run()
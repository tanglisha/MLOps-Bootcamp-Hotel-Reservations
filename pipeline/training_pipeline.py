from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from config.base_config import get_config

if "__main__" == __name__:
    # 1. Data ingestion
    data = DataIngestion()
    data.run()

    # 2. Data processing
    processor = DataProcessor()
    processor.run()

    #. Model training
    model = ModelTraining()
    model.run()
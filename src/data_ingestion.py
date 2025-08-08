from logging import config
import pandas as pd
from numpy.random import RandomState
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from config.base_config import Config, get_config

logger = get_logger(__name__)

class DataIngestion:
    config: Config

    def __init__(self):
        self.config = get_config()

    def download_data_file(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.config.data_ingestion.bucket_name)
            blob = bucket.blob(self.config.data_ingestion.bucket_filename)

            blob.download_to_filename(self.config.paths.raw_filepath)

            logger.info(f"file successfully downloaded from gcp to {self.config.paths.raw_filepath}")

        except Exception as e:
            logger.error("error downloading csv file from bucket")
            raise

    def split_data(self):
        logger.info("starting data split")
        data = pd.read_csv(self.config.paths.raw_filepath)
        rng = RandomState()
        train_data = data.sample(frac=self.config.data_ingestion.train_ratio, random_state=rng)
        test_data = data.loc[~data.index.isin(train_data.index)]
        train_data.to_csv(self.config.paths.train_filepath)
        test_data.to_csv(self.config.paths.test_filepath)
        logger.info("successfully split data")    

    def run(self):
        logger.info(f"starting data ingestion from bucket {self.config.data_ingestion.bucket_name} file {self.config.data_ingestion.bucket_filename}")
        self.download_data_file()
        self.split_data()    
        logger.info("data ingestion completed")

if "__main__" == __name__:
    config = get_config()
    obj = DataIngestion()
    obj.run()


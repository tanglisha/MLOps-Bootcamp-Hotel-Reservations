from pathlib import Path
from src.logger import get_logger
import yaml
import pandas as pd

logger = get_logger(__name__)

def read_yaml_file(filepath: Path):
    try:
        with open(filepath, "r") as handle:
            config = yaml.safe_load(handle)
            logger.info("sucessfully loaded yaml file")
        return config
    except Exception as e:
        logger.exception(f"Error reading yaml file: {filepath.absolute}", e)
        raise


def load_data(csv_path: Path|str) -> pd.DataFrame:
    # Make sure this is a path
    csv_path = Path(csv_path)

    try:
        logger.info(f"Beginning to load file {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Successfully loaded {csv_path}")
        return df
    except Exception as e:
        logger.exception(f"Failed to load {csv_path}", e)
        raise

class DataSplitter:
    def _split_df_by_booking_status(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        X = df.drop(columns=("booking_status"))
        y = df["booking_status"]
        return X, y

from pathlib import Path
from pydantic import BaseModel, computed_field

class Paths(BaseModel):
    raw_dir: Path = Path(__file__).parent.parent / "artifacts" / "raw"
    raw_filename: str = "raw.csv"
    train_filename: str = "train.csv"
    test_filename: str = "test.csv"

    config_path: Path = Path(__file__).parent / "config.yml"

    ############################## DATA PROCESSING ###############################
    processed_dir: Path = Path(__file__).parent.parent / "artifacts" / "processed"
    processed_training_data_filename: str = "processed_train.csv"
    processed_test_data_filename: str = "processed_test.csv"

    ############################## DATA PROCESSING ###############################
    model_dir: Path = Path(__file__).parent.parent / "artifacts" / "models"
    model_output_filename: str = "lgbm_model.pkl"

    @computed_field
    @property
    def model_output_filepath(self) -> Path:
        self.model_dir.mkdir(parents=True, exist_ok=True)
        return self.model_dir / self.model_output_filename

    @computed_field
    @property
    def raw_filepath(self) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        return self.raw_dir / self.raw_filename
    
    @computed_field
    @property
    def train_filepath(self) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        return self.raw_dir / self.train_filename

    @computed_field
    @property
    def test_filepath(self) -> Path:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        return self.raw_dir / self.test_filename
    
    @computed_field
    @property
    def processed_training_data_filepath(self) -> Path:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        return self.processed_dir / self.processed_training_data_filename

    @computed_field
    @property
    def processed_test_data_filepath(self) -> Path:
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        return self.processed_dir / self.processed_test_data_filename

from functools import lru_cache
from ipaddress import IPv4Address
from pydantic import BaseModel, IPvAnyAddress
from config.model_params import LightGPMParams, RandomSearchParams
from config.paths import Paths
from src.utils.common import read_yaml_file


class DataIngestionConfig(BaseModel):
    bucket_name: str
    bucket_filename: str
    train_ratio: float


class PreprocessingConfig(BaseModel):
    skewness_threshold: int = 5
    number_of_features: int = 10
    categorical_column_names: list[str] = [
        "type_of_meal_plan",
        "required_car_parking_space",
        "room_type_reserved",
        "market_segment_type",
        "repeated_guest",
        "booking_status",
    ]
    numerical_column_names: list[str] = [
        "no_of_adults",
        "no_of_children",
        "no_of_weekend_nights",
        "no_of_week_nights",
        "lead_time",
        "arrival_year",
        "arrival_month",
        "arrival_date",
        "no_of_previous_cancellations",
        "no_of_previous_bookings_not_canceled",
        "avg_price_per_room",
        "no_of_special_requests",
    ]


class Model(BaseModel):
    light_params: LightGPMParams
    random_search: RandomSearchParams


class Application(BaseModel):
    host: IPvAnyAddress = IPv4Address("0.0.0.0")
    port: int = 8080
    debug: bool = False


class Config(BaseModel):
    data_ingestion: DataIngestionConfig
    data_processing: PreprocessingConfig
    application: Application
    paths: Paths
    model: Model
    random_state: int = 42


@lru_cache()
def get_config():
    paths = Paths()
    paths.raw_dir.mkdir(parents=True, exist_ok=True)
    paths.processed_dir.mkdir(parents=True, exist_ok=True)

    config_path = paths.config_path

    data = read_yaml_file(config_path)
    model_params = Model(
        light_params=LightGPMParams(), random_search=RandomSearchParams()
    )
    return Config(**data, model=model_params, paths=paths)


config = get_config()

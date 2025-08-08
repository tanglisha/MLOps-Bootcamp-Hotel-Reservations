from typing import Iterable
from scipy.stats import randint, uniform
from pydantic import BaseModel, Field

class LightGPMParams(BaseModel):
    n_estimators: Iterable[int] = [randint(100, 500).rvs(),]
    max_depth: Iterable[int] = [randint(5, 50).rvs(),]
    learning_rate: Iterable[int] = [uniform(0.01, 0.2).rvs()]
    num_leaves: Iterable[int] = [randint(20, 100).rvs()]
    boosting_type: list = Field(default_factory=lambda: ["gbdt", "dart", "goss"])

class RandomSearchParams(BaseModel):
    n_iter: int = 4
    n_jobs: int = -1
    cv: int = Field(gt=1, default=2)
    verbose: int = 2
    random_state: int = 42
    scoring: str = "accuracy"
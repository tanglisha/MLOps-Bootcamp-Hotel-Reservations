from pathlib import Path
import logging
from datetime import datetime

logs_dir = "logs"
logs_path = Path(logs_dir)
logs_path.mkdir(exist_ok=True)

log_file_name = f"{datetime.now()}.log"

log_file = logs_path.joinpath(log_file_name)

logging.basicConfig(
    filename=log_file,
    format= "%(asctime)s | %(levelname)s | %(filename)s(%(funcName)s)#%(lineno)d | %(message)s"
)

def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
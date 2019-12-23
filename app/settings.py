import logging
from dataclasses import dataclass


@dataclass
class Settings:
    workers: int = 300
    queue_size: int = workers * 20

    log_level: int = logging.DEBUG
    log_format: str = '%(asctime)s - %(levelname)-5s - %(name)-20s: %(message)s'

import logging

from .main import main
from .settings import Settings

settings = Settings()

logging.basicConfig(
    format=settings.log_format,
    level=settings.log_level
)

main(settings)

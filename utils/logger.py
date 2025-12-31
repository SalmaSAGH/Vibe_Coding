import logging
import sys
from pathlib import Path
from config.settings import get_settings

def setup_logging():
    settings = get_settings()
    Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=settings.log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized at level {settings.log_level}")
    return logger

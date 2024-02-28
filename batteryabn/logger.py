import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging configuration
LOG_MAX_SIZE = 20 * 1024 * 1024  # 20 MB
LOG_DIR = "logs"
LOG_FILE_NAME = 'batteryabn.log'

# Create log directory if not exists
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# Create logger
logger = logging.getLogger('batteryabn')

# Set logger level
env = os.getenv('ENV', 'prod')  # 'prod' as default
logger.setLevel(logging.DEBUG if env == 'dev' else logging.INFO) # Set log level to DEBUG in development environment

# Stream Handler Configuration
stream_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] [%(name)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

# File Handler Configuration
file_formatter = logging.Formatter(
    '{ "time": "%(asctime)s", "timestamp": "%(created)f", "level": "%(levelname)s", '
    '"file": "%(filename)s:%(lineno)d", "name": "%(name)s", "thread": "%(threadName)s", '
    '"process": "%(process)d", "message": "%(message)s" }'
)
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=LOG_MAX_SIZE, backupCount=10, delay=True
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


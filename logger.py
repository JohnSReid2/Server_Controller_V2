import logging
from logging.handlers import RotatingFileHandler
import os

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

log_path = os.path.join(log_dir, 'app.log')

logger = logging.getLogger('server_controller')
logger.setLevel(logging.INFO)

# File handler with rotation (5 logs, 1MB each)
handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
import logging
from datetime import datetime


def log_with_time(message: str):
    logging.info(f"[{datetime.now().strftime('%H:%M:%S')}] - {message}")

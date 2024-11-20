import os
import logging
from datetime import datetime

def get_log_file_name():
    log_dir = 'logs'

    timestamp = datetime.now().strftime('%d_%m_%Y')
    counter = 1
    while True:
        file_name = f'{timestamp}.app_log_{counter:03d}.log'
        file_path = os.path.join(log_dir, file_name)
        if not os.path.exists(file_path):
            return f'{file_path}'
        counter += 1

def setup_logging():
    # Create a directory to store log files
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_name = get_log_file_name()
    file_handler = logging.FileHandler(file_name, mode='a')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Create a formatter and add it to the file handler

    # Create a formatter and add it to the console handler
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    file_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
import logging
import logging.handlers
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from colors import *


def set_logger(log_name: str = 'app', log_file: str = 'logs.log', console_level=logging.INFO, file_level=logging.DEBUG):
    class ColorFormatter(logging.Formatter):
        LEVEL_COLORS = {
            logging.DEBUG: LIGHT_BLUE,
            logging.INFO: GREEN,
            logging.WARNING: YELLOW,
            logging.ERROR: LIGHT_RED,
            logging.CRITICAL: RED
        }

        def format(self, record):
            record.asctime = self.formatTime(record)

            time = f"{DARK_GRAY}{record.asctime}{WHITE}"
            # name = f"{DARK_GRAY}{record.name}{WHITE}"
            level = f"{self.LEVEL_COLORS.get(record.levelno, DEFAULT)}{BOLD}{record.levelname}{RESET}{WHITE}"
            MESSAGE = f"{WHITE}{record.getMessage()}{WHITE}"
            filename = f"{DARK_GRAY}{record.filename}"
            funcname = f"{DARK_GRAY}{record.funcName}()"
            lineno = f"{DARK_GRAY}{record.lineno} line{RESET}"

            # format log message
            log_message = f"{time} - {level} |  {MESSAGE}  | {filename} · {funcname} · {lineno}"
            return log_message

        def formatTime(self, record, datefmt=None):
            log_time = datetime.fromtimestamp(record.created)
            if datefmt:
                return log_time.strftime(datefmt)
            return log_time.strftime('%H:%M:%S')

    class FileFormatter(logging.Formatter):
        def format(self, record):
            message = remove_colors(record.getMessage())
            log_message = f"{record.asctime} - " \
                          f"{record.name} - " \
                          f"{record.levelname.ljust(8)} |  " \
                          f"{message}  | " \
                          f"{record.filename} · " \
                          f"{record.funcName}() · " \
                          f"{record.lineno} line"
            return log_message

        def formatTime(self, record, datefmt=None):
            log_time = datetime.fromtimestamp(record.created)
            if datefmt:
                return log_time.strftime(datefmt)
            return log_time.strftime('%Y-%m-%d %H:%M:%S')

    log_directory = os.path.join(os.path.dirname(__file__), f'../logs/{log_name}')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file_path = os.path.join(log_directory, log_file)

    app_logger = logging.getLogger(log_name)
    app_logger.setLevel(console_level)

    console_handler = logging.StreamHandler()
    color_formatter = ColorFormatter()
    console_handler.setFormatter(color_formatter)

    # Console handler
    console_handler.setLevel(console_level)
    app_logger.addHandler(console_handler)

    # File handler (RotatingFileHandler)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding='utf-8')
    file_handler.setLevel(file_level)
    file_formatter = FileFormatter()
    file_handler.setFormatter(file_formatter)
    app_logger.addHandler(file_handler)

    return logging.getLogger(log_name)


logger = set_logger()

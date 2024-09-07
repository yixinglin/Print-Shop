import logging
import os
from logging.handlers import TimedRotatingFileHandler
from .config import Logging
from .config import server_config, client_config


def create_logger(log_conf: Logging, name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    path = os.path.join(log_conf.path, name)
    os.makedirs(path, exist_ok=True)

    # Create a file handler for INFO level logs
    info_file_handler = TimedRotatingFileHandler(os.path.join(path, "info.log"), encoding="utf-8",
                                                 when="W0", backupCount=log_conf.backup_count)  # 按周日切割日志
    info_file_handler.setLevel(logging.INFO)

    # Create a file handler for ERROR level logs
    error_file_handler = TimedRotatingFileHandler(os.path.join(path, "error.log"), encoding="utf-8",
                                                  when="W0", backupCount=log_conf.backup_count)
    error_file_handler.setLevel(logging.ERROR)

    # Create a formatter for the logs
    formatter = logging.Formatter(log_conf.format, log_conf.datefmt)
    info_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(info_file_handler)
    logger.addHandler(error_file_handler)
    return logger

server_logger = create_logger(server_config.logging, "server")
client_logger = create_logger(client_config.logging, "client")
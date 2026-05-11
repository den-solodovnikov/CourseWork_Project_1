import logging
from pathlib import Path

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def get_file_handler(name):
    current_file = Path(__file__).resolve()
    root_dir = current_file.parent.parent
    f_name = f'{root_dir}/logs/{name}.log'
    print(name, f_name, f_name)
    file_handler = logging.FileHandler(f_name, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(name))
    # logger.addHandler(get_stream_handler())
    return logger

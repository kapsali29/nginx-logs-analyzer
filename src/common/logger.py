import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name=None, level=logging.INFO, json_mode=False):
    """Logger implementation"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        if json_mode:
            handler.setFormatter(jsonlogger.JsonFormatter())
        else:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )
            handler.setFormatter(formatter)

        logger.addHandler(handler)
    return logger

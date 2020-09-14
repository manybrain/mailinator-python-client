import logging


LOG_FORMAT = '%(asctime)s :: %(levelname)8s :: %(filename)16s:%(lineno)3s :: %(message)s'
LOG_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'


def get_logger(appName='Console', logLevel=logging.INFO):
    logger = logging.getLogger(appName)

    logger.setLevel(logLevel)

    if not any([isinstance(handler, logging.StreamHandler) for handler in logger.handlers]):
        logger.addHandler(get_console_handler())

    return logger


def get_console_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    return handler

import coloredlogs
import logging

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def info(msg):
    logger.info(msg)

def warn(msg):
    logger.warn(msg)

def error(msg):
    logger.error(msg)
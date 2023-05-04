import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

logger.info('This is an information message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')

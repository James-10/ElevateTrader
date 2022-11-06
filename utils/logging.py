import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

LOGGER = logging.getLogger("etrade")

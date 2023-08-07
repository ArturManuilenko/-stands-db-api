import logging
import os


logging.basicConfig(
    level=os.environ.get('LOGLEVEL', logging.DEBUG),
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
)
logging.getLogger("pika").setLevel(logging.DEBUG)

logging.getLogger("unipipeline").setLevel(logging.DEBUG)

self_logging = logging

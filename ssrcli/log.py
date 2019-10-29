import os
import logging

if os.getenv('DEBUG', None):
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ssrcli')

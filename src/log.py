import sys
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

fh = logging.FileHandler('ruyibuild.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
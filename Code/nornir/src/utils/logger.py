from utils.constants import RESULTS_FILE
import logging

# Configure logging
logging.basicConfig(
    filename=RESULTS_FILE, 
    level=logging.DEBUG, 
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a'  # 'a' for append mode, 'w' for overwrite mode
)

# Get the logger
logger = logging.getLogger()



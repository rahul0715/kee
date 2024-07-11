import logging
from logging.handlers import RotatingFileHandler

# Configure the logging settings
logging.basicConfig(
    level=logging.ERROR,  # Set the default logging level to ERROR
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",  # Log message format
    datefmt="%d-%b-%y %H:%M:%S",  # Date format in the log messages
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),  # Log to a file with rotation
        logging.StreamHandler(),  # Log to the console
    ],
)

# Set the logging level for the pyrogram library to WARNING to reduce log verbosity
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Create a logger instance
logger = logging.getLogger()

# Test logging to verify configuration
logger.error("Logger is configured and ready.")

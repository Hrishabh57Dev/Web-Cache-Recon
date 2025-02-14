import logging
from datetime import datetime

def get_logger(module_name):
    """
    Sets up and returns a logger for the provided module name.
    Logs errors and exceptions to a file with timestamps.

    Args:
        module_name (str): Name of the module using the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.ERROR)

    # Create a file handler for error logging
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}_error.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)

    # Create a formatter and attach it to the file handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Attach the file handler to the logger
    if not logger.handlers:  # Avoid adding handlers multiple times
        logger.addHandler(file_handler)

    return logger

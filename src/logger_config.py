"""
Centralized logging configuration for the pipeline.
Import 'get_logger' anywhere you need a logger

"""
import logging

def get_logger(name:str) -> logging.Logger:
    """
    Returns a configured logger instance.
    Logs to both the console and a file (pipeline.log),
    with timestamps and level info included.
    """
    logger = logging.getLogger(name)

    # Prevent adding duplicate handlers if this is called multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt = "%Y- %m-%d %H:%M:%S ",
    )


    # Console handler — shows INFO and above on screen
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # File handler — writes everything (DEBUG and above) to a log file
    file_handler = logging.FileHandler("pipeline.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
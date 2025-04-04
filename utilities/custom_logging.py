import logging
import colorlog
import os


def clear_custom_log_file():
    # Dynamically determine the log directory relative to the current working directory
    log_dir = os.path.join('..', 'reports')
    log_file = 'my_custom.log'

    # Ensure that the directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Construct the full file path
    log_file_path = os.path.join(log_dir, log_file)

    # Clear the log file by opening it in write mode and immediately closing it
    with open(log_file_path, 'w'):
        pass


def get_custom_logger(name, log_level=logging.INFO):
    # Dynamically determine the log directory relative to the current working directory
    log_dir = os.path.join('..', 'reports')
    log_file = 'my_custom.log'

    # Construct the full file path
    log_file_path = os.path.join(log_dir, log_file)

    # Clear the log file before configuring the logger
    clear_custom_log_file()

    # Create a custom logger to avoid shadowing the outer logger
    custom_logger = logging.getLogger(name)

    # Check if the logger already has handlers and clear them to avoid duplicate handlers
    if custom_logger.hasHandlers():
        custom_logger.handlers.clear()

    custom_logger.setLevel(log_level)

    # Create a formatter for console with colors
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s',
        datefmt='%Y-%m-%d %I:%M:%S %p',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Create a formatter for the file without colors
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S %p'
    )

    # Create a file handler and use the dynamically constructed log file path
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(file_formatter)
    custom_logger.addHandler(file_handler)

    # Create a console handler with color formatting
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    custom_logger.addHandler(console_handler)

    return custom_logger


logger = get_custom_logger(__name__)


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"An error occurred in {func.__name__}: {e}")
            raise  # Re-raise exception to ensure the test fails

    return wrapper


def handle_exceptions_class(cls):
    """
    This decorator applies the `handle_exceptions_for_method` to all callable methods of the class.
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            # Apply the exception handler to each method
            setattr(cls, attr_name, handle_exceptions(attr_value))
    return cls

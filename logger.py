import logging


class Logger:
    def __init__(self):
        # Create a logger object
        self.logger = logging.getLogger(__name__)

        # Create a file handler and set the level to INFO
        file_handler = logging.FileHandler('mylog.log')
        file_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

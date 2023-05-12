import logging


class Logger:
    def __init__(self, name='mylog'):
        # Create a logger object
        print(name)
        self.logger = logging.getLogger(name)

        # Create a file handler and set the level to INFO
        file_handler = logging.FileHandler('logs/' + name + '.log')
        file_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

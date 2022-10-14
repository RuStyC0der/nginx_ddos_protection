import logging
import re
from dotenv import dotenv_values
from os import environ
from abstract.singleton import Singleton
from sys import stdout, stderr



def get_logger(name):

    config = Config()

    # Create a custom logger
    logger = logging.getLogger(name)

    logger.setLevel(str2LogLevel(config['LOG_LEVEL']))

    # Create handlers
    stdout_handler = logging.StreamHandler(stdout)
    file_handler = logging.FileHandler(config['LOG_FILE'])

    stdout_handler.setLevel(str2LogLevel(config['LOG_LEVEL']))
    file_handler.setLevel(str2LogLevel(config['LOG_LEVEL']))

    # Create formatters and add it to handlers
    formatter = logging.Formatter('{asctime} |{levelname:<8}| {name}: {message}', datefmt='%Y-%m-%d %H:%M:%S', style="{")

    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)

    return logger

def str2LogLevel(value):
	try:
		if isinstance(value, int) or value.isdigit():
			ll = int(value)
		else:
			ll = getattr(logging, value.upper())
	except AttributeError:
		raise ValueError(f"Invalid log level {value}")
	return ll

class Config(Singleton):
    
    _defaults_ = {
        "LOG_LEVEL":"INFO",
        "LOG_FILE":"nginx_ddos_protection.log",

        "SLEEP_ON_EMPTY_LOG_SECONDS":"0.5",
        "RATELIMIT":"300",
        "RATELIMIT_PERIOD_SECONDS":"60",

        "SOURCE_LOG_FILE":"/var/log/nginx/access.log",
    }

    def __init__(self):
        self.dotenv = dotenv_values()


    def get(self, key):
        """
        get value in priority:
        environment
        .env file
        defaults 
        """
        value = environ.get(key)
        if value:
            return value

        value = self.dotenv.get(key, None)
        if value:
            return value
        
        value = self._defaults_.get(key, None)
        if value:
            return value
        
        raise KeyError(f"Key '{key}' does not exist in config")


    def __getitem__(self, key):
        return self.get(key)

if __name__ == "__main__":
    c = Config()
    print(c['SOURCE_LOG_FILE'])

    logger = get_logger(__name__)

    logger.info("test")
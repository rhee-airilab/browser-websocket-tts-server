# coding: utf-8
import os
import sys
import logging
#logging.basicConfig()
from traceback import print_exc

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def getLogger(name):
    formatter = logging.Formatter(
        fmt='%(asctime)s %(filename)s:%(lineno)s: %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # default level

    logger.addHandler(console_handler)

    log_file_path = os.path.join(
            __location__,
            'logs/common-logs.txt')

    log_dir = os.path.dirname(log_file_path)
    if os.path.isdir(log_dir):
        file_handler = logging.FileHandler(log_file_path,mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

if __name__ == '__main__':
    logger = getLogger(__name__)
    logger.warn('Hello, World')


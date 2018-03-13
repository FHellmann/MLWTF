#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import os
import logging


class Config(object):
    """
    Common configurations
    """

    DEBUG = False

    basedir = os.path.abspath(os.path.dirname(__file__))

    DATABASE_URI = os.path.join(basedir, 'mysmarthome.db.json')

    _logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=_logFormatStr, level=logging.DEBUG)
    _logFormatter = logging.Formatter(_logFormatStr, '%m-%d %H:%M:%S')


class TestingConfig(Config):
    """
    Development configurations
    """

    DATABASE_URI = None

    TESTING = True

    LOG_HANDLER = logging.StreamHandler()
    LOG_HANDLER.setLevel(logging.INFO)
    LOG_HANDLER.setFormatter(Config._logFormatter)


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DATABASE_URI = os.path.join(Config.basedir, 'mysmarthome-dev.db.json')

    DEBUG = True

    LOG_HANDLER = logging.StreamHandler()
    LOG_HANDLER.setLevel(logging.DEBUG)
    LOG_HANDLER.setFormatter(Config._logFormatter)


class ProductionConfig(Config):
    """
    Production configurations
    """

    #LOG_HANDLER = logging.FileHandler("mysmarthome.log")
    LOG_HANDLER = logging.StreamHandler()
    LOG_HANDLER.setLevel(logging.ERROR)
    LOG_HANDLER.setFormatter(Config._logFormatter)


app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
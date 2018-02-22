#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging

from app import create_app

app = create_app()

if __name__ == '__main__':
    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')

    fileHandler = logging.FileHandler("smart_home.log")
    fileHandler.setLevel(logging.ERROR)
    fileHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(streamHandler)

    app.run(host='0.0.0.0', debug=True, port=5005)

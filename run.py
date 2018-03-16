#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import os

from app import create_app

env_name = os.getenv('FLASK_CONFIG')
app = create_app(env_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
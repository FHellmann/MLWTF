#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask_testing import TestCase

from app import create_app


class TestBase(TestCase):

    def create_app(self):
        # pass in test configuration
        config_name = 'testing'
        app = create_app(config_name)
        return app

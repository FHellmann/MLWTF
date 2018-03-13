#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import unittest
from flask import url_for

from tests import TestBase


class TestViews(TestBase):

    def test_home_view(self):
        """
        Test that home is accessible
        """
        response = self.client.get(url_for('home.index'))
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        """
        Test that settings is accessible
        """
        response = self.client.get(url_for('settings.index'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

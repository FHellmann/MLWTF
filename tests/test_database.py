#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import unittest

from . import TestBase

from app import db
from app.database.models import RfSignal


class TestModels(TestBase):

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test signals
        signal1 = RfSignal(code=350, bit_length=1)
        signal2 = RfSignal(code=530, bit_length=5)

        # save to database
        db.session.add(signal1)
        db.session.add(signal2)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

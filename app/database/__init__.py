#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists


db = SQLAlchemy()
session = db.session


def setup(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_uri = 'sqlite://'  # In-Memory usage for testing
    # database_uri = 'sqlite:///' + os.path.join(basedir, 'my-smart-home.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    with app.test_request_context():
        db.init_app(app)
        if not database_exists(database_uri):
                db.create_all()


def db_add(item):
    session.add(item)
    session.commit()


def db_delete(item):
    session.delete(item)
    session.commit()


def db_update():
    session.commit()


class RfSignal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    code = db.Column(db.Integer, nullable=False)
    pulse_length = db.Column(db.Integer, nullable=False, default=350)
    bit_length = db.Column(db.Integer, nullable=False)
    sync_high = db.Column(db.Integer, nullable=False, default=1)
    sync_low = db.Column(db.Integer, nullable=False, default=31)
    zero_high = db.Column(db.Integer, nullable=False, default=1)
    zero_low = db.Column(db.Integer, nullable=False, default=3)
    one_high = db.Column(db.Integer, nullable=False, default=3)
    one_low = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return '<RfSignal %r>' % self.id

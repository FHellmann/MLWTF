#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from flask import Flask, jsonify
from flask_restful import Resource, Api
from tinydb import TinyDB, Query

app = Flask(__name__)
api = Api(app.blueprints)
db = TinyDB('my_db.json')


# general class for Room preferences
class Area(Resource):
    def __init__(self, type):
        self.type = type
        self.query = Query()

    def get(self):
        return db.search(self.query.type == self.type)


# API
api.add_resource(Area('living_room').get(), '/living_room')
api.add_resource(Area('hall').get(), '/hall')
api.add_resource(Area('bedroom').get(), '/bedroom')
api.add_resource(Area('bathroom').get(), '/bathroom')
api.add_resource(Area('kitchen').get(), '/kitchen')
api.add_resource(Area('entrance').get(), '/entrance')
api.add_resource(Area('garden').get(), '/garden')


if __name__ == '__main__':
    app.run(port='5005')


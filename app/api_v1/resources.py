"""This is main module where can be found all Resources for api version 1.0."""
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
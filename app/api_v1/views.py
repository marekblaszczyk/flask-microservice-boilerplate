from flask import Blueprint
from flask_restful import Resource, Api
from app.api_v1.resources import HelloWorld

BLUEPRINT = Blueprint('api', __name__, url_prefix='/')
api = Api(BLUEPRINT)

api.add_resource(HelloWorld, '/', endpoint="/")
from flask import Blueprint
from flask_restx import Api
from auth import ns as auth
from user import ns as user
from property import ns as prop
from web_email import ns as email_change
from repo_mananger import ns as repo
from Route_Plan import ns as plan

blueprint = Blueprint('api_v1', __name__)

api = Api(blueprint,
          version='0.1',
          title='Rental Inspection System',
          description='COMP9900-H18C-ALL-PASS backend api for rental inspection system.'
          )

api.add_namespace(auth)
api.add_namespace(user)
api.add_namespace(prop)
api.add_namespace(email_change)
api.add_namespace(repo)
api.add_namespace(plan)

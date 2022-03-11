from flask import Flask
from flask_mail import Mail
from config import CONFIG, EMAIL
from model.database import DB
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# flask jwt: https://flask-jwt-extended.readthedocs.io/en/latest/


mail = Mail()
jwt = JWTManager()
db = DB()


def create_app(name):
    app = Flask(name, static_url_path='/')
    app.config.from_object(CONFIG)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)
    mail.init_app(app)
    return app

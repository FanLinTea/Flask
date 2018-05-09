from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import config
from api_1_0.auth import auth

db = SQLAlchemy()
mail = Mail()
boots = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)
    boots.init_app(app)

    app.register_blueprint(auth)

    return app
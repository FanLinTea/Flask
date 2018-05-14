# coding:utf8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import config
from flask_login import LoginManager


db = SQLAlchemy()
mail = Mail()
boots = Bootstrap()
login = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)
    boots.init_app(app)


    from api_1_0.auth import auth
    from api_1_0.erro import aerro
    app.register_blueprint(auth)
    app.register_blueprint(aerro)
    login.session_protection = 'strong'
    login.login_view = 'auth.login' # 没有权限的用户，将跳转的登陆页面
    login.init_app(app)

    return app
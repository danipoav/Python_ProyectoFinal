from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "danipoav"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.login_view = 'main.login'  
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app

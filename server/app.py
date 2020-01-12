import os
from flask import Flask, render_template, Blueprint, session
from userAPI import user_api, User, Event
from emailAPI import email_api
from db_instance import db

project_dir = os.path.dirname(os.path.abspath(__file__))
project_paths = project_dir.split("/")
project_paths.pop()
project_paths.append('db')
project_dir = "/".join(project_paths)





def create_app():
    app = Flask(__name__,
        static_folder = "./dist/static",
        template_folder = "./dist"
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "userdata.db"))
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    app.register_blueprint(user_api)
    app.register_blueprint(email_api)
    app.secret_key = os.environ["SECRET_KEY"]

    return app

def setup_database(app):
    with app.app_context():
        db.create_all()
        # db.drop_all()
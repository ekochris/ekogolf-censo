# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_path = os.path.join(base_dir, '..', 'templates')
    static_path = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import bp as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app

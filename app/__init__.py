from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnova.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    db.init_app(app)

    from .models import User  # Import models so they are registered
    from .routes import main  # Import blueprints/routes

    app.register_blueprint(main)

    return app

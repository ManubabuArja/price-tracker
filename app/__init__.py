import os
from flask import Flask
from dotenv import load_dotenv

from core.scheduler import start_scheduler


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    # Blueprints
    from .routes import main
    app.register_blueprint(main)

    # Start background scheduler
    start_scheduler(app)

    return app
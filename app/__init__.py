import os
from flask import Flask
from dotenv import load_dotenv

from core.scheduler import start_scheduler
from core.tracker import ensure_data_files


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

    # Ensure data files exist
    with app.app_context():
        ensure_data_files()

    # Blueprints
    from .routes import main
    app.register_blueprint(main)

    # Start background scheduler
    start_scheduler(app)

    return app
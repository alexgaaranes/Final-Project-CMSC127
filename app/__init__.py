from flask import Flask
from .db import initialize_db
from .routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    initialize_db(app.config)
    app.register_blueprint(main_bp)
    return app
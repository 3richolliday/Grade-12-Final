from flask import Flask
from config import Config
from app.sqla import sqla


def create_app(config_class=Config):
    
    # Initialize Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy
    sqla.init_app(app)

    @app.route("/")
    def index_view():
        return "<h1>Langauge Master</h1>"
    
    return app
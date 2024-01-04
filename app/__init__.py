from flask import Flask, render_template
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
        return render_template("index.html")
    
    return app
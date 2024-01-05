from flask import Flask, render_template
from config import Config
from app.sqla import sqla
from app.login import login_manager


def create_app(config_class=Config):
    
    # Initialize Flask
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy
    sqla.init_app(app)

    # Inititialize Flask-Login
    login_manager.init_app(app)

    # Initialize Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.assess import bp as assess_bp
    app.register_blueprint(assess_bp, url_prefix='/assess')

    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app
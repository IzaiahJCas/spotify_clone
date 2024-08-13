from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__, static_folder="../build", static_url_path="/")
    CORS(app)

    # Load environment variables
    load_dotenv()

    # Load configuration
    POSTGRES_URL = os.getenv('POSTGRES_URL')
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Define your models
    from .models import SongBook

    # Register blueprints (if you have any)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
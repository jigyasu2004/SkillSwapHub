import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Load environment variables from .env file
load_dotenv()

# Configure logging - reduce verbosity for production
log_level = logging.INFO if os.environ.get("FLASK_ENV") == "production" else logging.DEBUG
logging.basicConfig(level=log_level)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
cache = Cache()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "skill-swap-secret-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure caching
app.config['CACHE_TYPE'] = 'simple'  # Use 'redis' for production with Redis
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

# Configure the database with performance optimizations
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,  # Increase pool size
    "max_overflow": 20,  # Allow more overflow connections
    "pool_timeout": 30,  # Connection timeout
    "echo": False,  # Disable SQL query logging for performance
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
cache.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create all tables
    db.create_all()
    
    # Add sample data if tables are empty
    from utils import create_sample_data
    create_sample_data()

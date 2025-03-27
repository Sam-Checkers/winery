from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
bcrypt = Bcrypt()

# Create the Flask app
app = Flask(__name__)

# Load configuration
from config import Config
app.config.from_object(Config)

# Initialize extensions with app
CORS(app)
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

# Initialize migrate after db
migrate = Migrate(app, db)

# Import routes at the end to avoid circular imports
from winery import routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

# Initialize extensions without app
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
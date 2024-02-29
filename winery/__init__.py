from flask import Flask, request, render_template, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from winery.config import Config
from winery.models import db as root_db, login_manager, ma
from winery.models import db, Post

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)
app.config.from_object(Config)

app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

from winery import routes
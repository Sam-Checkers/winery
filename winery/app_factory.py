from flask import Flask
from flask_migrate import Migrate

def create_app(config_object=None):
    app = Flask(__name__)
    
    # Configure app
    if config_object is None:
        from config import Config
        config_object = Config
    
    app.config.from_object(config_object)
    
    # Initialize extensions
    from extensions import db, login_manager, ma, bcrypt, cors
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    
    # Initialize migrate explicitly
    migrate = Migrate(app, db)
    
    
    return app
from flask import Flask

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        # Import config if not provided
        from config import Config
        config_class = Config
    
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    from winery.extensions import db, login_manager, ma, bcrypt, migrate, CORS
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    # Register routes
    from winery.routes import register_routes
    register_routes(app)
    
    return app
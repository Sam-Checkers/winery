import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to production for security
    SECRET_KEY = os.environ.get('SECRET_KEY') or '12345'  # Consider a stronger default
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Recommended setting
    
    # Add SSL configuration for Neon if using DATABASE_URI
    if 'neon.tech' in SQLALCHEMY_DATABASE_URI and 'sslmode' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?sslmode=require'
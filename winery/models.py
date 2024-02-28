from datetime import datetime
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow 
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
db=SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, first_name='', last_name='', username='', email='', password='', g_auth_verify=False, token=''):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class ContactSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title','content']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
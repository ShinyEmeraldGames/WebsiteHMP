from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os.path import join, dirname, realpath
from datetime import datetime, timezone

app = Flask(__name__, static_folder='static', template_folder='templates')

# Set up rate limiting – 3 requests per minute for all routes
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute"]
)

app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:Heute0000@127.0.0.1/ImgWebsite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'sh83wzfahaskfdh286zssdsfm'

db = SQLAlchemy(app)

class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Float, default=0)

    # If you want to have a relationship with the Users table
    user = db.relationship('Users', back_populates='images')
    comments = db.relationship('Comments', back_populates='image')

class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    
    images = db.relationship('Images', back_populates='user')
    comments = db.relationship('Comments', back_populates='user')

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    image_id = db.Column(db.String(255), db.ForeignKey('images.id'), nullable=False)  # Foreign key to images
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users
    comment_text = db.Column(db.Text, nullable=False)  # Comment text cannot be null
    comment_date = db.Column(db.DateTime, default=db.func.current_timestamp())  # Default to current timestamp
    rating = db.Column(db.Integer, nullable=False)

    # Relationships
    image = db.relationship('Images', back_populates='comments')  # Assuming Images class has a comments relationship
    user = db.relationship('Users', back_populates='comments')      # Assuming User class has a comments relationship

with app.app_context():
    db.create_all()

from reviews import routes
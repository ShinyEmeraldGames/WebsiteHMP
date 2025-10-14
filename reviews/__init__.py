from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, realpath

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:Heute0000@127.0.0.1/ImgWebsite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sh83wzfahaskfdh286zssdsfm'

db = SQLAlchemy(app)

from reviews import routes
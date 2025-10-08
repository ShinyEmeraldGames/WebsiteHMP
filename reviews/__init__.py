from flask import Flask
from os.path import join, dirname, realpath

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB

from reviews import routes
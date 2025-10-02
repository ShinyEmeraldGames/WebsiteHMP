from flask import Flask

app = Flask(__name__)

from reviews import routes
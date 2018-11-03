from flask import Flask

app = Flask(__name__)

from views.ciphers import ciphers
import routes

app.register_blueprint(ciphers)

from flask import Flask, url_for

app = Flask(__name__)

from views.ciphers import ciphers
import routes

app.register_blueprint(ciphers)

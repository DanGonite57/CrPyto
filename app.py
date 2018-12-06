from flask import Flask

app = Flask(__name__)

from views import ciphers, tools, errors
import routes

errors.init(app)
app.register_blueprint(ciphers.ciphers)
app.register_blueprint(tools.tools)

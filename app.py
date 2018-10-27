import os
import sys
from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   send_from_directory)
from Processing import Decrypt

# create the application object
app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')


@app.route('/')
def root():
    return redirect(url_for("index"))


@app.route("/index.html")
def index():
    return render_template('index.html', title="CrPyto")


@app.route("/<cipher>.html", methods=["GET", "POST"])
def ciphers(cipher):
    if request.method == "POST":
        ciph = request.form["ciphInput"]
        result, score = Decrypt.decrypt(ciph, cipher)
        return render_template(f"ciphers/{cipher}.html", title=cipher.capitalize(), ciph=ciph, result=result, score=score)
    return render_template(f"ciphers/{cipher}.html", title=cipher.capitalize(), ciph="", result="", score=0)


@app.errorhandler(404)
@app.errorhandler(500)
def exception(e):
    return render_template(f"{str(e)}.html"), e


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
    # app.run()

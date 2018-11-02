import os

from flask import (redirect, render_template, request, send_from_directory,
                   url_for)

from app import app
from Formatting import SpaceAdd
from Processing import DetectEnglish


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
    from Processing import Decrypt
    ciph = result = ""
    score = 0
    if request.method == "POST":
        ciph = request.form["ciphInput"]
        result, _ = Decrypt.decrypt(ciph, cipher)
        result = SpaceAdd.add(result)
        score = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/{cipher}.html", title=cipher.capitalize(), ciph=ciph, result=result, score=score)


@app.route("/substitution.html", methods=["GET", "POST"])
def substitution():
    from Ciphers import Substitution
    ciph = result = ""
    score = 0
    vals = {}
    if request.method == "POST":
        ciph = request.form["ciphInput"]
        result, _, vals = Substitution.decrypt(ciph)
        result = SpaceAdd.add(result)
        score = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/substitution.html", title="Substitution", ciph=ciph, result=result, score=score, vals=vals)


@app.route("/transposition.html", methods=["GET", "POST"])
def transposition():
    from Ciphers import Transposition
    ciph = result = keylen = ""
    score = 0
    if request.method == "POST":
        ciph = request.form["ciphInput"]
        keylen = request.form["keylenInput"]
        result, _ = Transposition.decrypt(ciph, int(keylen))
        result = SpaceAdd.add(result)
        score = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/transposition.html", title="Transposition", ciph=ciph, result=result, score=score, keylen=keylen)


@app.errorhandler(404)
@app.errorhandler(500)
def exception(e):
    return render_template(f"{str(e)}.html"), e

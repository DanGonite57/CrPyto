from flask import redirect, render_template, url_for

from app import app


@app.route('/')
def root():
    return redirect(url_for("index"))


@app.route("/index.html")
def index():
    return render_template('index.html', title="CrPyto")


@app.errorhandler(404)
@app.errorhandler(500)
def exception(e):
    return render_template(f"{str(e)}.html"), e

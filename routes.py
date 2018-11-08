import os

from flask import redirect, render_template, send_from_directory, url_for

from app import app


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


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

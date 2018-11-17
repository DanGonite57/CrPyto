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
def exception(error):
    # return render_template(f"errors/{str(e)}.html"), e
    return render_template("errors/404.html", title="404", error=error), 404


@app.errorhandler(Exception)
def oof(error):
    print(error)
    return render_template("errors/500.html", title="500"), 500

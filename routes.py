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


@app.errorhandler(403)
def e403(error):
    # return render_template(f"errors/{str(e)}.html"), e
    return render_template("errors/403.html", title="403", error=error), 403


@app.errorhandler(404)
def e404(error):
    return render_template("errors/404.html", title="404", error=error), 404


@app.errorhandler(410)
def e410(error):
    return render_template("errors/410.html", title="410", error=error), 410


@app.errorhandler(500)
def e500(error):
    return render_template("errors/500.html", title="500", error=error), 500


@app.errorhandler(Exception)
def oof(error):
    return render_template("errors/500.html", title="500", error=error), 500

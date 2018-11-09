from flask import Blueprint, render_template

tools = Blueprint("tools", __name__, url_prefix="/tools")


@tools.route("/addspaces.html")
def addSpaces():
    return render_template("tools/addspaces.html")


@tools.route("/removespaces.html")
def removeSpaces():
    return render_template("tools/removespaces.html")


@tools.route("/removepunctuation.html")
def removePunctuation():
    return render_template("tools/removepunctuation.html")

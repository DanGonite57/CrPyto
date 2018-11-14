from flask import Blueprint, render_template, request

from Formatting import SpaceAdd
from Processing import DetectEnglish

tools = Blueprint("tools", __name__, url_prefix="/tools")


@tools.route("/addspaces.html")
def addSpaces():
    return render_template("tools/addspaces.html", title="Add Spaces")


@tools.route("/removespaces.html")
def removeSpaces():
    return render_template("tools/removespaces.html", title="Remove Spaces")


@tools.route("/removepunctuation.html")
def removePunctuation():
    return render_template("tools/removepunctuation.html", title="Remove Punctuation")


@tools.route("/reversetext.html", methods=["GET", "POST"])
def reverseText():
    args = {"title": "Reverse Text", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = ciph[::-1]
        args["score"] = DetectEnglish.detectWord(SpaceAdd.add(plain)) * 100
    return render_template(f"tools/reversetext.html", **args)

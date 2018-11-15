from flask import Blueprint, render_template, request

from Formatting import PuncRem, SpaceAdd, SpaceRem
from Processing import DetectEnglish

tools = Blueprint("tools", __name__, url_prefix="/tools")


@tools.route("/addspaces.html", methods=["GET", "POST"])
def addSpaces():
    args = {"title": "Add Spaces", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = SpaceAdd.add(ciph)
        args["score"] = DetectEnglish.detectWord(plain) * 100
    return render_template(f"tools/addspaces.html", **args)


@tools.route("/removespaces.html", methods=["GET", "POST"])
def removeSpaces():
    args = {"title": "Remove Spaces", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = SpaceRem.remove(ciph)
        args["score"] = DetectEnglish.detectWord(SpaceAdd.add(plain)) * 100
    return render_template(f"tools/removespaces.html", **args)


@tools.route("/removepunctuation.html", methods=["GET", "POST"])
def removePunctuation():
    args = {"title": "Remove Punctuation", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = PuncRem.remove(ciph)
        args["score"] = DetectEnglish.detectWord(SpaceAdd.add(plain)) * 100
    return render_template(f"tools/removepunctuation.html", **args)


@tools.route("/reversetext.html", methods=["GET", "POST"])
def reverseText():
    args = {"title": "Reverse Text", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = ciph[::-1]
        args["score"] = DetectEnglish.detectWord(SpaceAdd.add(plain)) * 100
    return render_template(f"tools/reversetext.html", **args)

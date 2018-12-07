from flask import Blueprint, abort, json, render_template, request

from Formatting import PuncRem, SpaceAdd, SpaceRem
from Processing import DetectEnglish

ciphers = Blueprint("ciphers", __name__, url_prefix="/ciphers")

METHODS = ["GET", "POST"]


@ciphers.route("/auto.html")
def auto():
    abort(501)


@ciphers.route("/caesar.html", methods=METHODS)
def caesar():
    args = {"title": "Caesar", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": "", "key": ""}
    if request.method == "POST":
        from Ciphers import Caesar

        ciphText = request.form["ciphInput"].lower()
        result, _ = Caesar.decrypt(ciphText)
        score = DetectEnglish.detect(SpaceAdd.add(result)) * 100

        args = {"title": "Caesar", "ciphText": ciphText, "result": result, "score": score}
    return render_template(f"ciphers/caesar.html", **args)


@ciphers.route("/substitution.html", methods=METHODS)
def substitution():
    args = {"title": "Substitution", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": "", "key": ""}
    if request.method == "POST":
        from Ciphers import Substitution

        ciphText = PuncRem.remove(request.form["ciphInput"]).lower()

        if request.form.get("useSpace"):
            result, vals = Substitution.decryptWithSpaces(ciphText)
        else:
            result, vals = Substitution.decrypt(ciphText)
        score = DetectEnglish.detectWord(SpaceAdd.add(result)) * 100

        args = {"title": "Substitution", "ciphText": ciphText, "result": result, "score": score, "vals": vals}
    return render_template(f"ciphers/substitution.html", **args)


@ciphers.route("/transposition.html", methods=METHODS)
def transposition():
    args = {"title": "Transposition", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": "", "key": ""}
    if request.method == "POST":
        from Ciphers import Transposition

        ciphText = PuncRem.remove(request.form["ciphInput"]).lower()
        keylen = int(request.form["keylenInput"] or 0)
        key = request.form["keyInput"]

        result, key = Transposition.decrypt(ciphText, key=key, keylen=keylen)
        key = ','.join(key)
        spacedResult = SpaceAdd.add(result)
        score = DetectEnglish.detectWord(spacedResult) * 100

        args = {"title": "Transposition", "ciphText": ciphText, "result": result, "score": score, "keylen": keylen, "key": key}
    return render_template(f"ciphers/transposition.html", **args)


@ciphers.route("/vigenere.html", methods=METHODS)
def vigenere():
    args = {"title": "Vigenere", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": "", "key": ""}
    if request.method == "POST":
        from Ciphers import Vigenere

        ciphText = request.form["ciphInput"]
        keylen = request.form["keylenInput"]
        key = request.form["keyInput"]

        result, key, _ = Vigenere.decrypt(ciphText, key=key, keylen=keylen)
        score = DetectEnglish.detectWord(SpaceAdd.add(result)) * 100

        args = {"title": "Vigenere", "ciphText": ciphText, "result": result, "score": score, "keylen": keylen, "key": key}
    return render_template(f"ciphers/vigenere.html", **args)


@ciphers.route("/subInputs", methods=METHODS)
def subInputs():
    if request.method == "POST":
        changed = request.json["name"][0]
        newval = request.json["val"].lower()
        if newval == "":
            newval = "_"
        ciphText = SpaceRem.remove(PuncRem.remove(request.json["ciph"])).lower()
        plainText = SpaceRem.remove(request.json["plain"].lower())
        if plainText == "":
            new = ''.join([newval if x in changed else "_" for x in ciphText])
        else:
            plainText = [x for x in plainText]
            for i, letter in enumerate(ciphText):
                if letter == changed:
                    plainText[i] = newval
            new = "".join(plainText)
        score = DetectEnglish.detectWord(SpaceAdd.add(new)) * 100
        return json.dumps({"plain": new, "score": f"{score}% certainty"})
    return "error"


@ciphers.route("/addSpaces", methods=METHODS)
def addSpaces():
    if request.method == "POST":
        plainText = SpaceRem.remove(request.json["plain"])
        plainText = SpaceAdd.add(plainText)
        score = DetectEnglish.detectWord(plainText) * 100
        return json.dumps({"plain": plainText, "score": f"{score}% certainty"})
    return "error"


@ciphers.route("/splitKey", methods=METHODS)
def splitKey():
    if request.method == "POST":
        key = PuncRem.remove(SpaceRem.remove(request.json["key"]))
        key = ','.join([x for x in key])
        return json.dumps({"key": key})
    return "error"

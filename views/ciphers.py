from importlib import import_module

from flask import Blueprint, json, render_template, request

from Formatting import PuncRem, SpaceAdd, SpaceRem
from Processing import DetectEnglish

ciphers = Blueprint("ciphers", __name__, url_prefix="/ciphers")


@ciphers.route("/<ciphname>.html", methods=["GET", "POST"])
def cipher(ciphname):
    ciphname = ciphname.lower()
    ciph = import_module("Ciphers." + ciphname.capitalize())
    args = {"title": ciphname.capitalize(), "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": "", "key": ""}
    if request.method == "POST":
        args["ciphText"] = ciphText = PuncRem.remove(request.form["ciphInput"]).lower()
        if ciphname == "substitution":
            if request.form.get("useSpace"):
                result, _, vals = ciph.decryptWithSpaces(ciphText)
                args["result"] = result
                args["vals"] = vals
                args["score"] = DetectEnglish.detectWord(result) * 100
                return render_template(f"ciphers/{ciphname}.html", **args)
            else:
                result, _, vals = ciph.decrypt(ciphText)
            args["vals"] = vals
        elif ciphname == "transposition":
            key = request.form["keyInput"]
            try:
                keylen = int(request.form["keylenInput"])
            except ValueError:
                keylen = 0
            args["keylen"] = keylen
            result, key = ciph.decrypt(ciphText, key=key, keylen=keylen)
            args["key"] = ','.join(key)
        elif ciphname == "vigenere":
            keylen = request.form["keylenInput"]
            try:
                result, _ = ciph.decrypt(ciphText, int(keylen))
            except ValueError:
                result, _ = ciph.decrypt(ciphText)
        else:
            result, _ = ciph.decrypt(ciphText)
        args["result"] = result
        result = SpaceAdd.add(result)
        args["score"] = DetectEnglish.detectWord(result) * 100
    return render_template(f"ciphers/{ciphname}.html", **args)


@ciphers.route("/subInputs", methods=["GET", "POST"])
def subInputs():
    if request.method == "POST":
        # from Ciphers import Substitution
        changed = request.json["name"][0]
        newval = request.json["val"]
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


@ciphers.route("/addSpaces", methods=["GET", "POST"])
def addSpaces():
    if request.method == "POST":
        plainText = SpaceRem.remove(request.json["plain"])
        plainText = SpaceAdd.add(plainText)
        score = DetectEnglish.detectWord(plainText) * 100
        return json.dumps({"plain": plainText, "score": f"{score}% certainty"})
    return "error"

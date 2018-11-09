import string
import sys
from importlib import import_module

from flask import Blueprint, json, render_template, request

from Formatting import PuncRem, SpaceAdd
from Processing import DetectEnglish

ciphers = Blueprint("ciphers", __name__, url_prefix="/ciphers")


@ciphers.route("/<ciphname>.html", methods=["GET", "POST"])
def cipher(ciphname):
    ALPH = string.ascii_lowercase
    ciphname = ciphname.lower()
    ciph = import_module("Ciphers." + ciphname.capitalize())
    args = {"title": ciphname.capitalize(), "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciphText = PuncRem.remove(request.form["ciphInput"]).lower()
        if ciphname == "substitution":
            vals = {x: ''.join([request.form[x + "Sub"]]) for x in ALPH}
            if not any([vals[x] for x in vals]):
                result, _, vals = ciph.decrypt(ciphText)
            else:
                _, result, vals = ciph.sub(ciphText, vals)
            args["vals"] = vals
        elif ciphname == "transposition":
            keylen = request.form["keylenInput"]
            result, _ = ciph.decrypt(ciphText, int(keylen))
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
        args["score"] = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/{ciphname}.html", **args)


@ciphers.route("/subInputs", methods=["GET", "POST"])
def subInputs():
    if request.method == "POST":
        # from Ciphers import Substitution
        changed = request.json["name"][0]
        newval = request.json["val"]
        if newval == "":
            newval = "_"
        ciphText = PuncRem.remove(request.json["ciph"]).lower()
        plainText = request.json["plain"].lower()
        if plainText == "":
            new = ciphText.replace(changed, newval)
        else:
            ciphText = [x for x in ciphText]
            plainText = [x for x in plainText]
            for i, letter in enumerate(ciphText):
                if letter == changed:
                    plainText[i] = newval
            new = "".join(plainText)
        return json.dumps({"plain": new})

    return "error"

import string
from importlib import import_module

from flask import Blueprint, render_template, request

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
        args["ciphText"] = ciphText = PuncRem.remove(request.form["ciphInput"])
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
        args["result"] = result = SpaceAdd.add(result)
        args["score"] = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/{ciphname}.html", **args)

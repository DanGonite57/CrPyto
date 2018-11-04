import string
from importlib import import_module

from flask import Blueprint, render_template, request

from Formatting import PuncRem, SpaceAdd
from Processing import DetectEnglish

ciphers = Blueprint("ciphers", __name__, url_prefix="/ciphers")


@ciphers.route("/<ciphname>.html", methods=["GET", "POST"])
def cipher(ciphname):
    ciphname = ciphname.lower()
    ciph = import_module("Ciphers." + ciphname.capitalize())
    args = {"title": ciphname.capitalize(), "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciphText = PuncRem.remove(request.form["ciphInput"])
        if ciphname.lower() == "substitution":
            vals = {}
            for x in string.ascii_lowercase:
                vals[x] = [request.form[x + "Sub"]]
                if vals[x] == [""]:
                    vals[x] = [letter for letter in string.ascii_lowercase]
            result, _, vals = ciph.decrypt(ciphText, vals)
            args["vals"] = vals
        elif ciphname.lower() == "transposition":
            keylen = request.form["keylenInput"]
            result, _ = ciph.decrypt(ciphText, int(keylen))
        else:
            result, _ = ciph.decrypt(ciphText)
        args["result"] = result = SpaceAdd.add(result)
        args["score"] = DetectEnglish.detectWord(result)
    return render_template(f"ciphers/{ciphname}.html", **args)

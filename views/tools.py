import io
from string import ascii_lowercase as ALPH

from flask import Blueprint, Response, json, render_template, request
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from Formatting import PuncRem, SpaceAdd, SpaceRem
from Processing import DetectEnglish, FindAnagrams, FreqAnalysis

tools = Blueprint("tools", __name__, url_prefix="/tools")

METHODS = ["GET", "POST"]


@tools.route("/findanagrams.html", methods=METHODS)
def findAnagrams():
    args = {"title": "Find Anagrams", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = word = request.form["ciphInput"]
        args["plainText"] = "\n".join(FindAnagrams.find(word))
    return render_template(f"tools/findanagrams.html", **args)


@tools.route("/freqanalysis.html", methods=METHODS)
def freqAnalysis():
    args = {"title": "Frequency Analysis", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = request.form["ciphInput"]
    plotFreq(args["ciphText"])
    return render_template(f"tools/freqanalysis.html", **args)


@tools.route("/reversetext.html", methods=METHODS)
def reverseText():
    args = {"title": "Reverse Text", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    if request.method == "POST":
        args["ciphText"] = ciph = request.form["ciphInput"]
        args["result"] = plain = ciph[::-1]
        args["score"] = DetectEnglish.detectWord(SpaceAdd.add(plain)) * 100
    return render_template(f"tools/reversetext.html", **args)


@tools.route("/formatting.html", methods=METHODS)
def formatting():
    args = {"title": "Formatting", "ciphText": "", "result": "", "score": 0, "vals": {}, "keylen": ""}
    return render_template(f"tools/formatting.html", **args)


@tools.route("/addSpaces", methods=METHODS)
def addSpaces():
    if request.method == "POST":
        plainText = SpaceRem.remove(request.json["plain"])
        plainText = SpaceAdd.add(plainText)
        score = DetectEnglish.detectWord(plainText) * 100
        return json.dumps({"plain": plainText, "score": f"{score}% certainty"})
    return "error"


@tools.route("/remSpaces", methods=METHODS)
def remSpaces():
    if request.method == "POST":
        plainText = SpaceRem.remove(request.json["plain"])
        text = SpaceAdd.add(plainText)
        score = DetectEnglish.detectWord(text) * 100
        return json.dumps({"plain": plainText, "score": f"{score}% certainty"})
    return "error"


@tools.route("/remPunc", methods=METHODS)
def remPunc():
    if request.method == "POST":
        plainText = PuncRem.remove(request.json["plain"])
        text = SpaceAdd.add(plainText)
        score = DetectEnglish.detectWord(text) * 100
        return json.dumps({"plain": plainText, "score": f"{score}% certainty"})
    return "error"


@tools.route("/freqanalysis.png?<ciph>")
def plotFreq(ciph):
    ciph = SpaceRem.remove(PuncRem.remove(ciph.lower()))
    fig, ax = plt.subplots(figsize=(10, 5))
    barwidth = 0.3

    lettcounts = [FreqAnalysis.englishProbabilities.get(x, 0) for x in ALPH]
    ciphprobs = FreqAnalysis.getFrequencies(ciph)

    lettplot = []
    for x in range(26):
        lettplot.append(x - (barwidth / 2))
    ax.bar(lettplot, lettcounts, width=barwidth, label="English", color="r")
    try:
        ciphcounts = [ciphprobs.get(x, 0) / len(ciph) for x in ALPH]
        ciphplot = []
        for x in range(26):
            ciphplot.append(x + (barwidth / 2))
        ax.bar(ciphplot, ciphcounts, width=barwidth, label="Cipher Text", color="b")
    except ZeroDivisionError:
        pass
    ax.get_yaxis().set_visible(False)
    ax.set_xticks(range(26))
    ax.set_xticklabels(ALPH.upper())
    ax.legend()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

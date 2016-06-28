from __future__ import print_function
from flask import Flask, Markup, render_template, request
import time
from Talos.talos import *
from Talos.DCEC_Library.DCECContainer import DCECContainer

app = Flask(__name__)


@app.route('/')
def entry():
    return render_template('index.html')


@app.route('/prove', methods=['POST'])
def run_talos():
    t = time.time()

    prototypes = str(request.values.get('prototypes').strip()).split("#")
    axioms = str(request.values.get('axioms').strip()).split("#")
    conjecture = str(request.values.get('conjecture').strip())

    dcec_container = DCECContainer()
    dcec_container.namespace.addBasicDCEC()
    dcec_container.namespace.addBasicLogic()
    dcec_container.namespace.addBasicNumerics()

    for prototype in prototypes:
        if len(prototype) == 0:
            continue
        dcec_container.namespace.addTextFunction(prototype)

    ctr = 0
    for axiom in axioms:
        print(axiom)
        if len(axiom) != 0 and not dcec_container.addStatement(axiom):
            return "ERROR ON LINE %d" % ctr
        ctr += 1

    print("start")
    spass = spassContainer(dcec_container, conjecture, True, timeout=10, rules=spassContainer.temporalRules.keys() + spassContainer.basicLogicRules.keys())

    t = time.time() - t

    return_string = ""
    if spass.result[0] != "Error Found":
        return_string += spass.result[0] + "\n"
        return_string += "Proof:\n"
        for line in str(spass.proofToString()):
            return_string += line.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        return_string += "\n"
    else:
        return_string += "Errors:\n"
        return_string += spass.input + ("\n" * 3) + "\n"
        return_string += spass.errors + "\n"

    return_string += "Ran for " + str(round(t * 10000) / 10000) + " seconds.\n"
    print("done")
    return Markup(return_string.replace("\n", "<br />"))


if __name__ == "__main__":
    port = os.getenv('PORT', 5000)
    app.run(host='0.0.0.0', port=int(port))

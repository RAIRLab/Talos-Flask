"""
Flask application for running the Talos automated theorem prover
"""

from __future__ import print_function
import os
import time

from flask import Flask, Markup, render_template, request
from Talos.talos import SpassContainer
from Talos.DCEC_Library.dcec_container import DCECContainer

APP = Flask(__name__)


@APP.route('/')
def entry():
    """
    Display main index page where the user can enter formulas and defintions to run
    against the Talos prover

    :return: rendered template of index
    """
    return render_template('index.html')


@APP.route('/prove', methods=['POST'])
def run_talos():
    """
    Given what the user inputted, run it against the Talos prover, outputting the parsed respose
    in string format

    :return: string containing Talos response of proof attempt
    """
    run_time = time.time()

    prototypes = str(request.values.get('prototypes').strip()).split("#")
    axioms = str(request.values.get('axioms').strip()).split("#")
    conjecture = str(request.values.get('conjecture').strip())

    dcec_container = DCECContainer()
    dcec_container.namespace.add_basic_dcec()
    dcec_container.namespace.add_basic_logic()
    dcec_container.namespace.add_basic_numerics()

    for prototype in prototypes:
        if len(prototype) == 0:
            continue
        dcec_container.namespace.add_text_function(prototype)

    ctr = 0
    for axiom in axioms:
        if len(axiom) != 0 and not dcec_container.addStatement(axiom):
            return "ERROR ON LINE %d" % ctr
        ctr += 1

    spass = SpassContainer(dcec_container, conjecture, True, timeout=10,
                           rules=["MODUS_PONENS", "CONJUNCTION_INTRODUCTION"])

    run_time = time.time() - run_time

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

    return_string += "Ran for " + str(round(run_time * 10000) / 10000) + " seconds.\n"
    return Markup(return_string.replace("\n", "<br />"))


if __name__ == "__main__":
    PORT = os.getenv('PORT', 5000)
    APP.run(host='0.0.0.0', port=int(PORT))

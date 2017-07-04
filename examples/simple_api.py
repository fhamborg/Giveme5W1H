import logging
import os
import sys

# Add path to allow execution though console
sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from flask import Flask, request, jsonify
from extractor.document import Document
from extractor.extractor import FiveWExtractor
from extractor.preprocessors.preprocessor_core_nlp import Preprocessor

"""
This is a simple example on how to use flask to create a rest api for our extractor.

Please update the CoreNLP address to match your host and check the flask settings.
"""

# basic configuration of the rest api
app = Flask(__name__)
log = logging.getLogger(__name__)
host = None
port = 5000
debug = False
options = None

# CoreNLP host
core_nlp_host = 'localhost:9000'

# initialize the logger
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
log.addHandler(sh)
log.setLevel(logging.DEBUG)

# initialize all modules
preprocessor = Preprocessor(core_nlp_host)
extractor = FiveWExtractor(preprocessor)
log.info("extractor initialized")


# define route for parsing requests
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    json_article = request.get_json()
    log.debug("retrieved raw article for extraction: %s", json_article['title'])

    document = Document(json_article['title'], json_article['description'], json_article['text'])
    extractor.parse(document)

    return jsonify(document.get_answers())


if __name__ == "__main__":
    log.info("starting server on port %i", port)
    app.run(host, port, debug)
    log.info("server has stopped")

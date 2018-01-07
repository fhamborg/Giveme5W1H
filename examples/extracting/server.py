import logging
import socket

from flask import Flask, request, jsonify
from jinja2 import Environment, PackageLoader, select_autoescape

from extractor.document import Document
from extractor.extractor import FiveWExtractor
from extractor.tools.file.reader import Reader
from extractor.tools.file.writer import Writer

# - - from Giveme5W_enhancer.heideltime import Heideltime
# - - from Giveme5W_enhancer.aida import Aida

"""
This is a simple example on how to use flask to create a rest api for our extractor.

Please update the CoreNLP address to match your host and check the flask settings.
"""


# helper to find own ip address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


# Flask setup
app = Flask(__name__)
log = logging.getLogger(__name__)
host = get_ip()
port = 9099
debug = False

# Template engine
env = Environment(
    loader=PackageLoader('examples', 'extracting'),
    autoescape=select_autoescape(['html', 'xml'])
)

# Render landing page
template_index = env.get_template('index.html')

# Giveme5W setup
extractor = FiveWExtractor()

# extractor_enhancer = FiveWExtractor( enhancement=[
#    Heideltime(['when']),
#    Aida(['how','when','why','where','what','who'])
# ])
reader = Reader()
writer = Writer()


def get_mainPage():
    return template_index.render()


# define route for parsing requests
@app.route('/', methods=['GET'])
def root():
    return get_mainPage()


def request_to_document():
    if request.method == 'POST':
        data = request.get_json(force=True)
        document = reader.parse_newsplease(data, 'Server')
    elif request.method == 'GET':
        title = request.args.get('title', None)
        description = request.args.get('description', None)
        text = request.args.get('text', None)
        date = request.args.get('date', None)

        if title and (description or text):
            log.debug("retrieved raw article for extraction: %s", title)
            document = Document(title, description if description else '', text if text else '', date=date)
    return document


# define route for parsing requests
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    document = request_to_document()
    if document:
        extractor.parse(document)
        answer = writer.generate_json(document)
        return jsonify(answer)


# define route for parsing requests
# @app.route('/extractEnhancer', methods=['GET', 'POST'])
# def extractEnhancer():
#    document = request_to_document()
#    if document:
#        #extractor_enhancer.parse(document)
#        answer = writer.generate_json(document)
#        return jsonify(answer)


if __name__ == "__main__":
    # setup config
    # Config.get()["candidate"]["nlpIndexSentence"] = False
    # Config.get()["candidate"]["part"]['nlpTag'] = False
    # Config.get()["candidate"]["score"] = False
    # Config.get()["label"] = False
    # Config.get()["onlyTopCandidate"] = True

    # startup
    log.info("starting server on port %i", port)
    app.run(host, port, debug)

    log.info("server has stopped")

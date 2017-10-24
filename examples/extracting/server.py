import datetime
import logging
import os
import sys
import time
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('examples', 'extracting'),
    autoescape=select_autoescape(['html', 'xml'])
)

sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from flask import Flask, request, jsonify
from extractor.document import Document
from extractor.extractor import FiveWExtractor
from extractor.tools.file.writer import Writer
from extractor.tools.file.reader import Reader
from extractor.configuration import Configuration as Config

"""
This is a simple example on how to use flask to create a rest api for our extractor.

Please update the CoreNLP address to match your host and check the flask settings.
"""




import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# basic configuration of the rest api
app = Flask(__name__)
log = logging.getLogger(__name__)
host = get_ip()
port = 9099
debug = False

# setup config
#Config.get()["candidate"]["nlpIndexSentence"] = False
#Config.get()["candidate"]["part"]['nlpTag'] = False
#Config.get()["candidate"]["score"] = False
#Config.get()["label"] = False

Config.get()["onlyTopCandidate"] = True


extractor = FiveWExtractor()

reader = Reader()
writer = Writer()

template_index = env.get_template('index.html')

# im sure there is a smarter way... this is a very simple landing page
def get_mainPage():

    return template_index.render()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    example_link = "/extract?title=While%20the%20U.S.%20talks%20about%20election,%20UK%20outraged%20over%20Toblerone%20chocolate&text=Skip%20Ad%20Ad%20Loading...%20x%20Embed%20x%20Share%20Toblerone%20is%20facing%20a%20mountain%20of%20criticism%20for%20changing%20the%20shape%20of%20its%20famous%20triangular%20candy%20bars%20in%20British%20stores,%20a%20move%20it%20blames%20on%20rising%20costs.%20USA%20TODAY%20Toblerone%20chocolate%20bars%20come%20in%20a%20variety%20of%20sizes,%20but%20recently%20changed%20the%20shape%20of%20two%20of%20its%20smaller%20bars%20sold%20in%20the%20UK.%20(Photo:%20Martin%20Ruetschi,%20AP)%20The%20UK%20has%20a%20chocolate%20bar%20crisis%20on%20its%20hands:%20the%20beloved%20Swiss%20chocolate%20bar%20is%20unrecognizable."

    response = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
    response += '<title>giveme5W REST API</title>'
    response += ''

    response += "<p>Provide title and (text or description) for GET. Keep in mind to encode special characters</p>"
    response += "<p>For POST, use the newsplease format, use the form below for example</p>"
    response += "<form action='/extract' method='post'>"
    response += "<p><a href='" + example_link + "'>GET example</a></p>"
    response += timestamp
    response += '</head><body>'
    response += '</body ></html >'

    return response

# define route for parsing requests
@app.route('/', methods=['GET'])
def root():
    return get_mainPage()

# define route for parsing requests
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    title = None
    description = None
    text = None

    if request.method == 'POST':
        data = request.get_json(force=True)
        document = reader.parse_newsplease(data,'Server')
    elif request.method == 'GET':
        title = request.args.get('title', None)
        description = request.args.get('description', None)
        text = request.args.get('text', None)

        if title and (description or text):
            log.debug("retrieved raw article for extraction: %s", title)
            document = Document(title, description if description else '', text if text else '')

    if document:
        extractor.parse(document)

        answer = writer.generate_json(document)
        # writer was initial written for files.
        # Files-Object is wrapping the results under fiveWoneH
        #return answer # jsonify(answer.get('fiveWoneH'))
        return jsonify(answer)

    else:
        return get_mainPage()


if __name__ == "__main__":
    log.info("starting server on port %i", port)
    app.run(host, port, debug)
    log.info("server has stopped")

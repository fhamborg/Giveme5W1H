from livereload import Server, shell
from flask import Flask, current_app, send_from_directory

app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
    app.logger.info('Info: index.html')
    return current_app.send_static_file('webapp/index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file('webapp/'+path)

@app.route('/resources/<path:path>')
def framework(path):
    app.logger.info(path)
    return app.send_static_file('resources/'+path)

@app.route('/data/<path:path>')
def data(path):
    app.logger.info(path)
    return send_from_directory('../data/',path)


server = Server(app.wsgi_app)
# server.watch
server.serve()
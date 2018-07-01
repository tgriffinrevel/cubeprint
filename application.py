from flask import Flask, request
from get_proxies import runner

application = Flask(__name__)


@application.route('/')
@application.route('/index')
def index():
    decks = request.args.get('decks').split(',')
    identity = request.args.get('identity') == 'true'
    return runner(decks, identity)

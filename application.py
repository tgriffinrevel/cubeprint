from flask import Flask
from get_proxies import runner
application = Flask(__name__)

@application.route('/')
@application.route('/index')
def index():
    return runner(['1150953'], False)
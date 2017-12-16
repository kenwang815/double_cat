# -*- coding: UTF-8 -*-
import logging.config
from flask import Flask, Blueprint, request, g
from config import Config
import time
from . import api_1_0
from .persistence import model
from . import util

log = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1', template_folder='templates')
api_1_0.init(blueprint)

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    log.debug(u"request: {}".format(u' '.join([request.remote_addr, request.method, request.url])))
    model.open_connection()


@app.after_request
def after_request(response):
    model.close_connection()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS, HEAD, PATCH')
    response.headers.add('Access-Control-Max-Age', '86400')
    response.headers.add('x-time-elpased', g.request_time())
    return response


@util.log_scope(log)
def create_app():
    app.config.from_object(Config)
    Config.init_app(app)
    model.init(app)

    return app

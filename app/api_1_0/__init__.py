# -*- coding: UTF-8 -*-
import flask_restplus
import logging
from .. import util


log = logging.getLogger(__name__)
api = flask_restplus.Api(version='1.0', title='DC API', description='Double Cat API')


@util.log_scope(log)
def init(app):
    api.init_app(app)

    from . import category_endpoint
    from . import task_endponit

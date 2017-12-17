# -*- coding: UTF-8 -*-
import logging
from . import util
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from .persistence import model


log = logging.getLogger(__name__)


class AdminModel(ModelView):
    can_create = False
    can_delete = False


@util.log_scope(log)
def init(app):
    admin = Admin(app, name='double_cat', template_mode='bootstrap3')
    admin.add_view(AdminModel(model.Category))
    admin.add_view(AdminModel(model.Image))
    log.info('inited.')

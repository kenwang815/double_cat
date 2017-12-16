# -*- coding: UTF-8 -*-
import logging
from .. import util
from ..persistence.model import Category
from peewee import IntegrityError

log = logging.getLogger(__name__)


@util.log_scope(log)
def create(name, count, url):
    log.debug(name)
    log.debug(count)
    log.debug(url)
    try:
        p = Category.create(name=name, count=count, url=url)
        return p
    except IntegrityError as e:
        log.debug(e)

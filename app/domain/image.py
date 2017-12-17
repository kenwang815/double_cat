# -*- coding: UTF-8 -*-
import logging
from .. import util
from ..persistence.model import Image
from peewee import IntegrityError

log = logging.getLogger(__name__)


@util.log_scope(log)
def create(name, extension, size, unit, width, height, url):
    try:
        p = Image.create(name=name, extension=extension, size=size, unit=unit, width=width, height=height, url=url)
        return p
    except IntegrityError as e:
        log.debug(e)

# -*- coding: UTF-8 -*-
import logging
from .. import util
from ..persistence.model import Image, Category_Image
from peewee import IntegrityError

log = logging.getLogger(__name__)


@util.log_scope(log)
def create(category_id, name, extension, size, unit, width, height, url):
    try:
        image_id = Image.create(name=name, extension=extension, size=size, unit=unit, width=width, height=height, url=url)
        Category_Image.create(category=category_id, image=image_id)
    except IntegrityError as e:
        log.debug(e)


@util.log_scope(log)
def find(category_id, page_number, items_per_page):
    rows = Image.select().join(Category_Image).where(Category_Image.category_id == category_id).paginate(page_number, items_per_page)

    return list(rows)

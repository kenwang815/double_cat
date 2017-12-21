# -*- coding: UTF-8 -*-
import logging
from .. import util
from ..persistence.model import Category, Image, Category_Image
from peewee import IntegrityError

log = logging.getLogger(__name__)


@util.log_scope(log)
def create(name, count, url):
    try:
        p = Category.create(name=name, count=count, url=url)
        return p
    except IntegrityError as e:
        log.debug(e)


@util.log_scope(log)
def find_all(page_number=1, items_per_page=25):
    rows = Category.select().paginate(page_number, items_per_page).execute()
    return list(rows)


@util.log_scope(log)
def find_children(category_id, page_number=1, items_per_page=25):
    query = Category.select().where(Category.id == category_id)
    if query.count() == 0:
        raise Exception()

    rows = Image.select().join(Category_Image).where(Category_Image.category_id == category_id).paginate(page_number, items_per_page).execute()
    return list(rows)

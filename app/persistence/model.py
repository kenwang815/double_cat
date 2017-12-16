# -*- coding: UTF-8 -*-
from peewee import *
import logging
import config
import os

log = logging.getLogger(__name__)
database_proxy = Proxy()


def open_connection():
    database_proxy.connect()


def close_connection():
    database_proxy.close()


class BaseModel(Model):
    name = CharField(index=True, unique=True, constraints=[Check('name <> \'\'')])
    created_date = DateTimeField(index=True, constraints=[SQL('DEFAULT (datetime(\'now\', \'localtime\'))')])
    modified_date = DateTimeField(null=True)

    def __unicode__(self):
        return u'<{}:{}>'.format(self.id, self.name)

    class Meta:
        database = database_proxy


class Category(BaseModel):
    count = IntegerField(default=0, index=True)
    url = CharField(null=True, index=True)


def init(app):
    if app.config['DEBUG']:
        database = SqliteDatabase(config.sqlite_db)
    elif app.config['TESTING']:
        database = SqliteDatabase(':memory:')
    else:
        database = PostgresqlDatabase('mega_production_db')

    database_proxy.initialize(database)
    if not os.path.isfile(config.sqlite_db):
        database.create_table(Category)
    database_proxy.close()

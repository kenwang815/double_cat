# -*- coding: UTF-8 -*-
export_folder = "src"
download_folder = "images"
url = "http://rthost.cr.rs/sd/"
sqlite_db = "double_cat.db"


class Config(object):
    HOST_NAME = '0.0.0.0'
    SERVER_PORT = 8080
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'double_cat'

    @staticmethod
    def init_app(app):
        pass

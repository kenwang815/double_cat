# -*- coding: UTF-8 -*-
from flask_restplus import fields, reqparse

from . import api

base_filter = reqparse.RequestParser()
base_filter.add_argument('page_number', type=int, default=1, help=u'頁碼')
base_filter.add_argument('items_per_page', type=int, default=25, help=u'每頁顯示筆數, -1 means fetch all records.')

category_query = api.model('category_query', {
    'id': fields.Integer(required=True, description=u'id', example=u'1'),
    'name': fields.String(required=True, description=u'類別名稱', example=u'饅饅來祭'),
    'count': fields.Integer(required=True, description=u'數量'),
    'url': fields.String(required=True, description=u'來源', example=u'http://rthost.cr.rs/sd/pixmicat.php?res=383048'),
})

images_query = api.model('category_images_query', {
    'id': fields.Integer(required=True, description=u'id', example=u'1'),
    'size': fields.Integer(required=True, description=u'檔案大小', example=u'100'),
    'unit': fields.String(required=True, description=u'單位', example=u'KB'),
    'width': fields.Integer(required=True, description=u'寬', example=u'480'),
    'height': fields.Integer(required=True, description=u'高', example=u'720'),
    'url': fields.String(required=True, description=u'來源', example=u'http://rthost.cr.rs/sd/pixmicat.php?res=383048'),
})

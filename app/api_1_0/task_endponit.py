# -*- coding: UTF-8 -*-
from flask import jsonify, request
from flask_restplus import Resource
from . import api
from ..adapter import double_cat
from ..domain import category as Category
from ..domain import image as Image


namespace = api.namespace('task', description=u'背景任務')


@namespace.route('')
class Import(Resource):
    @api.response(201, 'Success')
    def post(self):
        """
        start collection data.
        """
        page_links = double_cat.get_all_page_link()
        for page_link in page_links:
            category_links = double_cat.get_category_list(page_link)
            for category in category_links:
                img_links = double_cat.collect_image_link(category)
                category["count"] = img_links.__len__()
                category_id = Category.create(**category)

                for img_info in img_links:
                    Image.create(category_id, **img_info)

        return None, 201

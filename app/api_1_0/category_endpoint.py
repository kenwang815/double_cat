# -*- coding: UTF-8 -*-
from flask import jsonify, request
from flask_restplus import Resource
from . import category_endpoint_model as model
from . import api
from ..domain import category


namespace = api.namespace('category', description=u'主題類別')


@namespace.route('')
class Collection(Resource):
    @api.expect(model.base_filter)
    @api.marshal_with(model.category_query)
    @api.response(200, 'Success')
    def get(self):
        """
        Get all category.
        """
        args = model.base_filter.parse_args(request)
        return category.find_all(**args)


@namespace.route('/<int:id>/images')
class Image(Resource):
    @api.expect(model.base_filter)
    @api.marshal_with(model.images_query)
    @api.response(200, 'Success')
    def get(self, id):
        """
        Get songs in category.
        """
        args = model.base_filter.parse_args(request)
        return category.find_children(id, **args)

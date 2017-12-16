# -*- coding: UTF-8 -*-
from flask import jsonify, request
from flask_restplus import Resource
from . import api


namespace = api.namespace('category', description=u'主題類別')


@namespace.route('')
class Collection(Resource):
    @api.response(200, 'Success')
    def get(self):
        """
        get all category.
        """
        return jsonify(data=["aa", "bb"])

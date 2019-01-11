# -*- coding: utf-8 -*-
from odoo import http

# class Basedata(http.Controller):
#     @http.route('/basedata/basedata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/basedata/basedata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('basedata.listing', {
#             'root': '/basedata/basedata',
#             'objects': http.request.env['basedata.basedata'].search([]),
#         })

#     @http.route('/basedata/basedata/objects/<model("basedata.basedata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('basedata.object', {
#             'object': obj
#         })
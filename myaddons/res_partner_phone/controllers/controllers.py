# -*- coding: utf-8 -*-
from odoo import http

# class InheritPurchase(http.Controller):
#     @http.route('/inherit_purchase/inherit_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_purchase/inherit_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_purchase.listing', {
#             'root': '/inherit_purchase/inherit_purchase',
#             'objects': http.request.env['inherit_purchase.inherit_purchase'].search([]),
#         })

#     @http.route('/inherit_purchase/inherit_purchase/objects/<model("inherit_purchase.inherit_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_purchase.object', {
#             'object': obj
#         })
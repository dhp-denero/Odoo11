# -*- coding: utf-8 -*-
from odoo import http

# class ServiceCenter(http.Controller):
#     @http.route('/service_center/service_center/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/service_center/service_center/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('service_center.listing', {
#             'root': '/service_center/service_center',
#             'objects': http.request.env['service_center.service_center'].search([]),
#         })

#     @http.route('/service_center/service_center/objects/<model("service_center.service_center"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('service_center.object', {
#             'object': obj
#         })
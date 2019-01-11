# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteRequirement(http.Controller):
#     @http.route('/website_requirement/website_requirement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

# #     @http.route('/website_requirement/website_requirement/objects/', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('website_requirement.listing', {
# #             'root': '/website_requirement/website_requirement',
# #             'objects': http.request.env['website_requirement.website_requirement'].search([]),
# #         })

# #     @http.route('/website_requirement/website_requirement/objects/<model("website_requirement.website_requirement"):obj>/', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('website_requirement.object', {
# #             'object': obj
# #         })
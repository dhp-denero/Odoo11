# -*- coding: utf-8 -*-
from odoo import http

# class DocumentPreview(http.Controller):
#     @http.route('/document_preview/document_preview/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/document_preview/document_preview/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('document_preview.listing', {
#             'root': '/document_preview/document_preview',
#             'objects': http.request.env['document_preview.document_preview'].search([]),
#         })

#     @http.route('/document_preview/document_preview/objects/<model("document_preview.document_preview"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('document_preview.object', {
#             'object': obj
#         })
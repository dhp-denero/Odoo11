# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class document_preview(models.Model):
#     _name = 'document_preview.document_preview'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class document_preview(models.Model):
	_inherit = "ir.attachment"

	doc_url = fields.Char(compute="_compute_url")

	@api.one
	def _compute_url(self):
		base_url = self.env["ir.config_parameter"].search([("key", "=", "web.base.url")]).value
		self.doc_url = "https://docs.google.com/gview?url=" + base_url + '/web/image/%s?unique=%s' % (self.id, self.checksum)
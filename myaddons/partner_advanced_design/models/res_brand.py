# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResBrand(models.Model):
    _name = 'res.brand'
    _description = 'Brand'

    name = fields.Char(string='Name')
    description = fields.Text('Description', translate=True)
    logo = fields.Binary('Logo File')
    partner_count = fields.Integer('Partner', compute='_get_partner_count')
    product_count = fields.Integer('Product', compute='_get_product_count')

    @api.one
    def _get_partner_count(self):
        self.partner_count = len(self.partner_ids)

    @api.one
    def _get_product_count(self):
        self.product_count = len(self.product_ids)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(
        'res.brand',
        string='Brand',
        help='Select a brand for this product'
    )
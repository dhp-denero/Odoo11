# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Product(models.Model):
    """在产品中加入海关编码、中文品名、规格型号、原产目的国、成交单位和币种字段"""
    _description = 'add the Country of originOrCountry of destination'
    _inherit = 'product.template'

    hs_code = fields.Many2one('product_hs_code', string='HS code')              # 海关编码
    hs_code_cname = fields.Char('Chinese Name', related='hs_code.G_Name')       # 中文品名
    specifications = fields.Char('Specifications')                              # 规格型号
    delegate_country = fields.Many2one(
        'customs_basedata.delegate_country',
        string='Origin Or Destination Country')                                 # 原产国/目的国
    unit = fields.Many2one('turnover_unit', string='Unit')              # 成交单位
    currency = fields.Many2one('currency_system', string='Currency')    # 币种
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Delegation_product_data(models.Model):
    """委托清单中产品列表的产品模型"""
    _name = 'delegate_product_data'
    _description = 'a product data for delegation list'

    product_id = fields.Many2one('product.product', string='产品名称', domain=[('sale_ok', '=', True)], ondelete='restrict')
    hs_code = fields.Many2one('product_hs_code', string='HS code')  # hs_code
    chinese_name = fields.Char('中文品名', compute='_get_hs_code_name', store=True)

    specifications = fields.Char('规格型号')
    qty_invoiced = fields.Float(string='成交数量')
    unit = fields.Many2one('turnover_unit', '成交单位')
    price_unit = fields.Float('单价')
    price_subtotal = fields.Float(string='成交总价')
    currency = fields.Many2one('currency_system', '币制')
    delegate_country = fields.Many2one('delegate_country', '原产国/目的国')

    product_list_id = fields.Many2one('delegation_list', '委托清单')    # 关联委托清单

    @api.depends('hs_code')
    def _get_hs_code_name(self):
        for item in self:
            item.chinese_name = item.hs_code.G_Name




class Delegation_product_data_send(models.Model):
    '''委托清单已发送后，产品列表的产品模型'''
    _name = 'delegate_product_data_send'
    _description = 'a product data for delegation list has send'

    hs_code = fields.Char('HS Code')
    chinese_name = fields.Char('中文品名')
    english_name = fields.Char('英文品名')

    specifications = fields.Char('规格型号')
    product_uom_qty = fields.Float(string='成交数量')
    product_uom = fields.Char('成交单位')
    price_unit = fields.Float('单价')
    price_subtotal = fields.Float(string='成交总价')
    currency = fields.Char('币制')
    country_id = fields.Char('原产国/目的国')
    product_list_id = fields.Many2one('delegation_list', '委托清单')    # 关联已发送后的委托清单





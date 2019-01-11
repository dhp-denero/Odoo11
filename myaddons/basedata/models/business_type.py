# -*- coding: utf-8 -*-
from odoo import models, fields, api, _



class BusinessType(models.Model):
    """业务类型"""

    _name = "business_type"
    _description = "business type for work sheet"
    _table = "business_type"

    name = fields.Char(string="Name", size=50)
    in_out = fields.Selection(string='InOut', selection=[('i', 'import'), ('e', 'export')])
    transport_mode = fields.Many2one(comodel_name='delegate_transport_mode', string='Transport Mode')

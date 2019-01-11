# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    """在客户信息上加入统一社会信用代码、海关编码和检验检疫注册编码字段，针对于公司"""
    _description = 'partner added Uniform Social Credit Code'
    _inherit = 'res.partner'

    USCC = fields.Char('USCC')      # 统一社会信用代码
    HS = fields.Char('HS Code')     # 海关编码
    CIQ = fields.Char('CIQ Code')   # 检验检疫注册编码

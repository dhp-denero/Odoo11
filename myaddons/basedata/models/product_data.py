# -*- coding: utf-8 -*-
from odoo import models, fields


class HSCode(models.Model):
    """报关商品编码数据"""
    _name = 'product_hs_code'
    _description = 'add the Country of originOrCountry of destination'
    _rec_name = 'Code_TS'
    _table = 'b_hg_complex'

    Code_TS = fields.Char('HS Code', size=50)  # 海关编码
    G_Name = fields.Char('Chinese Name', size=100)    # 中文品名
    # LegalUN = fields.Char('法定单位', size=50)
    # SecondUN = fields.Integer('第二单位')
    # Control_Ma = fields.Char('Regulatory Tag', size=255)  # 监管标识


class DeclareElement(models.Model):
    """报关商品申报要素"""
    _name = 'declare_element'
    _description = 'add declare element to delegation'
    _rec_name = 'HSCode_TS'
    _table = 'b_hg_complex_criterion'

    HSCode_TS = fields.Char('HS Code', size=255)   # 海关编码
    CriterionName = fields.Char('Element Name', size=255)   # 要素名
    Orders = fields.Char('Num', size=255)   # 序号


class Country(models.Model):
    """国家、地区"""
    _name = 'delegate_country'
    _description = 'add the Country of originOrCountry of destination'
    _rec_name = 'NameCN'
    _table = 'b_hg_country'

    Code = fields.Char('Country Code', size=50)     # 国家代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class Unit(models.Model):
    """商品单位"""
    _name = 'turnover_unit'
    _description = 'add special unit for delegation'
    _rec_name = 'NameCN'
    _table = 'b_hg_unit'

    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称
    Code = fields.Char('Unit Code', size=50)        # 单位代码


class CurrencySystem(models.Model):
    """币种"""
    _name = 'currency_system'
    _description = 'add special currency system for delegation'
    _rec_name = 'NameCN'
    _table = 'b_hg_currency'

    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称
    Code = fields.Char('Currency Code', size=50)     # 币种代码

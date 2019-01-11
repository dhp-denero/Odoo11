# -*- coding: utf-8 -*-
from odoo import models, fields


class TransportMode(models.Model):
    """运输方式"""
    _name = 'delegate_transport_mode'
    _description = 'Mode of transport'
    _table = 'b_hg_traf_mode'
    _rec_name = 'name_cn'

    code = fields.Char(string='Transport Mode Code', size=50)       # 运输方式代码
    name_cn = fields.Char(string='Chinese Name', size=50)     # 中文名称


class Exemption(models.Model):
    """征免性质"""
    _name = 'delegate_exemption'
    _description = 'exemption nature of delegation'
    _table = 'b_hg_cut_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Exemption Code', size=50)       # 征免方式代码
    NameCN = fields.Char('Chinese Name', size=50)       # 中文名称


class TradeTerms(models.Model):
    """成交方式"""
    _name = 'delegate_trade_terms'
    _description = 'trade terms of delegation'
    _table = 'b_hg_trans_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Terms Code', size=50)   # 成交方式代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class Port(models.Model):
    """装运港"""
    _name = 'delegate_port'
    _description = 'ports of delegation'
    _table = 'b_hg_port'
    _rec_name = 'NameCN'

    Code = fields.Char('Port Code', size=50)     # 装运港代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class Customs(models.Model):
    """进出口岸"""
    _name = 'delegate_customs'
    _description = 'customs of delegation'
    _table = 'b_hg_customs'
    _rec_name = 'NameCN'

    Code = fields.Char('Custom Code', size=50)     # 进出口岸代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class TradeMode(models.Model):
    """监管方式"""
    _name = 'delegate_trade_mode'
    _description = 'trade mode of delegation'
    _table = 'b_hg_trade_mode'
    _rec_name = 'NameCN'

    Code = fields.Char('Trade Mode Code', size=50)     # 监管方式代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class Region(models.Model):
    """境内目的地"""
    _name = 'delegate_region'
    _description = 'region of delegation'
    _table = 'b_hg_district_code'
    _rec_name = 'NameCN'

    Code = fields.Char('Region Code', size=50)     # 境内目的地代码
    NameCN = fields.Char('Chinese Name', size=50)   # 中文名称


class Packing(models.Model):
    """包装方式"""
    _name = 'delegate_packing'
    _description = 'packing of delegation'
    _table = 'b_hg_wrap_type'
    _rec_name = 'NameCN'

    Code = fields.Char("Pack Code", size=50)     # 包装种类代码
    NameCN = fields.Char("Chinese Name", size=50)   # 中文名称
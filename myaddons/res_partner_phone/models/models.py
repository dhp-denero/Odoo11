# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_phone_ids = fields.One2many('res.partner.phone', 'partner_id')


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _description = '联系人联系方式'

    # name = fields.Selection(string='Type')
    number_or_username = fields.Char(string='Number or Username')
    tags = fields.Many2many('res.partner.phone.tags', string='Tags')
    note = fields.Char(string='Note')
    partner_id = fields.Many2one('res.partner')


class ResPartnerPhoneTags(models.Model):
    _name = 'res.partner.phone.tags'
    _description = '标签'

    name = fields.Char(string='Type')


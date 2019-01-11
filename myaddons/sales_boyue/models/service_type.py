# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ServiceType(models.Model):
    '''服务类型'''
    _name = 'service_type'
    _description = 'service type in delegation message'

    name = fields.Char('类型')

    _sql_constraints = [
        ('name_unique', 'unique(name)', '类型名必须唯一')
    ]
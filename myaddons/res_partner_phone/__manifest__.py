# -*- coding: utf-8 -*-
{
    'name': "res_partner_phone",

    'summary': """Partner Phone Number Module""",

    'description': """
        Partner Phone Number
    """,

    'author': "COMESOON",
    'website': "http://www.comesoon.hk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Partner Phone',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
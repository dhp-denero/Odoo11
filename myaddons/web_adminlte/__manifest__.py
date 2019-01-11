# -*- coding: utf-8 -*-
{
    'name': 'AdminLTE Backend Theme',
    "summary": "Odoo 11.0 community adminlte backend theme",
    'category': 'Themes/Backend',
    'author': 'Comesoon Kenneth',
    'version': '11.0.1.0.0',
    'description': '',
    'depends': ['web'],
    'data': [
        'views/assets.xml',
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'auto_install': False

}

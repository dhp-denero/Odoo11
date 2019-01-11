# -*- coding: utf-8 -*-
{
    'name': "Document Preview",

    'summary': """
        Preview any type of document using Google view""",

    'description': """
        Supporting .doc, .docx, xls, xlsx, pdf, ppt, pptx
    """,

    'author': "Magestore",
    'website': "http://www.magestore.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    'installable': True,
    'application': False,
}

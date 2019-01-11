# -*- coding: utf-8 -*-
{
    'name': "服务中心",

    'summary': """
        在客服处理工作单
       """,

    'description': """
        建立工作单模型，可以直接从工作单中生成销售订单。工作单模型里有基本信息、货物信息、发运信息、服务类型和委托商品信息。
    """,

    'author': "周杨",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['basedata', 'mail'],

    # always loaded
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/work_sheet_views.xml',
        'views/custom_declaration_draft.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ]
}
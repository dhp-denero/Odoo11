# -*- coding: utf-8 -*-
{
    'name': "销售扩展模块",

    'summary': """
        在原有的销售模块中加入报关的功能
        """,

    'description': """
        扩展的功能：
        1. 加入各种海关数据，对其建模.
        2. 在客户信息上加入统一社会信用代码和海关编码.
        3. 订单和产品上加入各种报关参数.
        4. 在相应的销售和产品视图上显示报关参数.
        5. 能生成委托清单，产生XML报文.
        6. 能与公司的交换系统对接.
    """,

    'author': "周杨 王志强",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'customs_basedata'],

    # always loaded
    'data': [
        'views/sale_custom.xml',
        'views/product.xml',
        'views/order.xml',
        'views/delegation_list/delegation_list.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/quotes.xml',
        'report/quote_report.xml',
        'data/mail_template_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
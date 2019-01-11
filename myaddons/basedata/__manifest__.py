# -*- coding: utf-8 -*-
{
    'name': "基础数据",

    'summary': """
        维护所有新添加的基础数据
        """,

    'description': """
        添加商品中的HS编码、申报要素、国家地区、商品单位、币种和报关单中的运输方式、
        免征性质、成交方式、装运港、进出口岸、监管方式、境内目的地、包装方式。
        将“产品类别”改为“服务费用类别”、在产品中只显示服务费用项。
    """,

    'author': "周杨 王志强",
    'website': "http://www.aeotrade.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/product_category_data.xml',
        'data/transport_mode_data.xml',
        'data/business_type.xml',
        'views/product_template_views.xml',
        'views/country.xml',
        'views/currency_system.xml',
        'views/customs.xml',
        'views/declare_element.xml',
        'views/exemption.xml',
        'views/hs_code.xml',
        'views/packing.xml',
        'views/port.xml',
        'views/region.xml',
        'views/trade_mode.xml',
        'views/trade_terms.xml',
        'views/transport_mode.xml',
        'views/unit.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
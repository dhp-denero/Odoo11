# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Requirement Geolocation',
    'version': '2.0',
    'category': 'Sales',
    'author': 'Kenneth',
    'description': """
Requirement Geolocation
Custom From Partner Geolocation
========================
    """,
    'depends': ['base','web_google_maps','sale_requirement'],
    'data': [
        'views/sale_requirement_views.xml',
    ],
    'installable': True,
}

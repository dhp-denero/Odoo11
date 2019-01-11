# Copyright 2017 - 2018 Modoolar <info@modoolar.com>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).
{
    'name': 'Booststrap TreeView',
    'version': '1.0',
    'category': 'web',
    'sequence': 14,
    'license':'LGPL-3',
    'description': """
    Web Widget BootstrapTreeView
    """,
    'author': 'COMESOON Kenneth',
    'website': 'comesoon.hk',
    'images': [],
    'depends': ['web'],
    'qweb': [
        "static/src/xml/bootstraptree.xml",
    ],
    'data': [
        'views/assets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

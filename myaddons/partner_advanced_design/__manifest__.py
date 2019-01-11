# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Partner Extend",
    'version': '11.0.1',
    'summary': """Extend Partner Form""",
    'description': """Extend Partner Form""",
    'author': "Kenneth",
    'website': "https://www.comesoon.hk",
    'category': 'Sales',
    'depends': ['base', 'product'],
    'data': [
            'security/ir.model.access.csv',
            'views/partner_views_form_inherit.xml',
            'views/res_brand.xml',
             ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

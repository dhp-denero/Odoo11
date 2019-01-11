# See LICENSE file for full copyright and licensing details.

{
    'name': 'HR-MISSING',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'Manage missing of employee',
    'author': 'Comesoon Kenneth',
    'category': 'Human Resources',
    'website': 'https://www.comesoon.hk',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_model_access_security.xml',
        'views/hr_missing_view.xml',
    ],
    'images': ['static/description/HRGradeRank.png'],
    'licence': 'AGPL-3',
    'sequence': 1,
    'installable': True,
    'auto_install': False,
}

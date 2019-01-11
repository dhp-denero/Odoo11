# See LICENSE file for full copyright and licensing details.

{
    'name': 'hr.applicant-plus',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'Manage hr applicant',
    'author': 'Comesoon Kenneth',
    'category': 'Human Resources',
    'website': 'https://www.comesoon.hk',
    'depends': ['hr','hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_model_access_security.xml',
        'views/hr_applicant_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'licence': 'AGPL-3',
    'sequence': 1,
    'installable': True,
    'auto_install': False,
}

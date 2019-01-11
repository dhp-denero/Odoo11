# See LICENSE file for full copyright and licensing details.

{
    'name': 'HR-Performance',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'summary': 'Managing the performance of employee,for calculating the salary for employee.',
    'author': 'Comesoon Kenneth',
    'category': 'Human Resources',
    'website': 'https://www.comesoon.hk',
    'depends': ['hr','account','hr_timesheet','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_model_access_security.xml',
        'views/hr_performance_view.xml',
    ],
    'images': ['static/description/HRGradeRank.png'],
    'licence': 'AGPL-3',
    'sequence': 1,
    'installable': True,
    'auto_install': False,
}

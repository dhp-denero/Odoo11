{
    'name': "SW - HR Attendance ZKTecho",

    'summary': """
        Integration with ZKTecho Biometric Devices
        """,

    'description': """
                """,

    'author': "Smart Way Business Solutions",
    'website': "https://www.smartway-jo.com",

    'category': 'Attendance',
    'version': '11.0.1.0',

    'depends': ['base', 'hr', 'hr_payroll', 'hr_contract', 'hr_attendance', 'mail', 'resource'],
    
    'data': [
        'data/get_attendance.xml',
        'security/biometricdevice_security.xml',
        'security/ir.model.access.csv',
        'views/company_view.xml',
        'views/hr_attendance_view.xml',
        'views/biometricdevice_view.xml',
        'views/hr_extensionview.xml',
        'wizard/move_attendance_wizard_view.xml',
        'wizard/generate_missing_attendance.xml',
    ],
    
    "images":  ['static/description/zkteco.png'],
    "price"    :  160,
    "currency" :  "EUR",
    'installable': True,
    'auto_install':False,
    'application':False,
    
}
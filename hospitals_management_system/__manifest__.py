{
    'name': 'Hospitals Management System App',
    'summary': 'To manage hospital',
    'description': '',
    'author': 'Assem Ashraf',
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': [
        'base',
        'crm'
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/base_menus.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'views/res_partner.xml',
        'views/website.xml',
        'views/vat.xml',
        'wizard/add_patient_log_wizard_view.xml',
        'report/patient_print.xml'
    ]
}

# -*- coding: utf-8 -*-
{
    'name': "(POS) Restrict employees access in the POS.",
    'summary': "Restrict the access in the POS from a specific user/employee.",
    'description': "Restrict the access in the POS from a specific user/employee.",
    'author': "Sayed Ahmed Abbas Ahmed",
    'category': 'Point of Sale',
    'version': '1.0',
    'price': 0.00,
    'currency': 'USD',
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
    'depends': ['point_of_sale', 'hr', 'pos_hr'],
    'data': [
        'security/ir_module_category_data.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/hr_employee_views.xml',
        'views/pos_restrict_access_template.xml',
    ],
}
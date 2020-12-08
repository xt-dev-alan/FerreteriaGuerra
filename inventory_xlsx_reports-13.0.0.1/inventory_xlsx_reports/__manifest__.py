# -*- coding: utf-8 -*-
{
    'name': "Inventory xlsx Reports",

    'summary': """
        
        """,

    'description': """
    """,
    'author': "Abdalmola Mustafa",
    'website': "mailto:abdalmolamustafa23@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'license': 'OPL-1',
    'category': 'report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale_stock', 'purchase_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/wizard_view.xml',
    ],
    # only loaded in demonstration mode
    'images': ['static/description/product_details.png', 'static/description/product_move.png',
               'static/description/icon.png'],
    'demo': [
        'demo/demo.xml',
    ],
}

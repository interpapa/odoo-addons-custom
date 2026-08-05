# -*- coding: utf-8 -*-
{
    'name': 'Smart Excel Mass Update',
    'version': '18.0.1.0.0',
    'summary': 'Mass update products effortlessly using Excel without complex External IDs.',
    'description': """
        Smart Excel Mass Update
        =======================
        Eliminate the headache of Odoo's native import engine. 
        This module allows you to select products, download a smart Excel template, 
        update the prices/names in Excel, and re-upload to instantly update the database.
        
        Features:
        - 1-Click Template Generation.
        - Fail-Safe mechanism (skips invalid rows instead of crashing).
        - Detailed success/error logging.
    """,
    'category': 'Extra Tools',
    'author': 'David Gil',
    'license': 'OPL-1',
    'price': 147.00,
    'currency': 'EUR',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/smart_excel_update_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
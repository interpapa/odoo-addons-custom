# -*- coding: utf-8 -*-
{
    'name': 'Visual Packing Slip: Images on Delivery Reports',
    'version': '16.0.1.0.0',
    'summary': 'Prevent packing mistakes. Add large product images to your Odoo delivery slips.',
    'description': """
        Visual Packing Slip
        ===================
        This premium module enhances the native Odoo Delivery Slip (Packing Slip):
        - Adds large product images directly into the delivery report PDF.
        - Enables faster visual verification during the packing process.
        - Reduces mis-packs and shipping errors by giving operators visual confirmation.
        
        Strictly non-destructive and OCA standard compliant.
    """,
    'author': 'David Gil',
    'category': 'Inventory/Inventory',
    'license': 'OPL-1',
    'price': 49.99,
    'currency': 'EUR',
    'depends': ['stock'],
    'data': [
        'views/report_deliveryslip_inherited.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
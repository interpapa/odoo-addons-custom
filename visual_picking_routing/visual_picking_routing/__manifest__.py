# -*- coding: utf-8 -*-
{
    'name': 'Visual Picking Routing',
    'version': '17.0.1.0.0',
    'summary': 'Optimized picking routes and visual product identification for warehouse operators.',
    'description': """
        Visual Picking Routing
        ======================
        This premium module extends the native Odoo Inventory capabilities:
        - Adds product images (thumbnails) to the picking operations PDF report.
        - Automatically reorders printed lines based on source location to minimize operator walking distance.
        - Enlarges barcodes on the printed document for faster and more reliable scanning.
        
        Strictly non-destructive and OCA standard compliant.
    """,
    'author': 'David Gil',
    'category': 'Inventory/Inventory',
    'license': 'OPL-1',
    'price': 49.99,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'depends': ['stock'],
    'data': [
        'views/report_picking_inherited.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

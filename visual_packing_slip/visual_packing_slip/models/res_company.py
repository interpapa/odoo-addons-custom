# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    visual_packing_enable_images = fields.Boolean(
        string='Enable Images on Packing Slip', 
        default=True,
        help="Turn on/off product images on the delivery slip PDF."
    )
    visual_packing_image_size = fields.Selection([
        ('small', 'Small (60px)'),
        ('medium', 'Medium (90px)'),
        ('large', 'Large (120px)')
    ], string='Packing Image Size', default='medium')
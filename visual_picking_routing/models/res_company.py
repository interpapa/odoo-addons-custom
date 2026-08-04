# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    visual_picking_enable_images = fields.Boolean(
        string='Enable Images on Picking', 
        default=True,
        help="Turn on/off product images on the picking operations PDF."
    )
    visual_picking_image_size = fields.Selection([
        ('small', 'Small (60px)'),
        ('medium', 'Medium (90px)'),
        ('large', 'Large (120px)')
    ], string='Image Size', default='medium')
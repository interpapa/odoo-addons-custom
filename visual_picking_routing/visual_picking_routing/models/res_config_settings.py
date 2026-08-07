# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    visual_picking_enable_images = fields.Boolean(
        related='company_id.visual_picking_enable_images', 
        readonly=False
    )
    visual_picking_image_size = fields.Selection(
        related='company_id.visual_picking_image_size', 
        readonly=False
    )
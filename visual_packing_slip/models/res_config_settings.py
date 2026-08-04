# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    visual_packing_enable_images = fields.Boolean(
        related='company_id.visual_packing_enable_images', 
        readonly=False
    )
    visual_packing_image_size = fields.Selection(
        related='company_id.visual_packing_image_size', 
        readonly=False
    )
# -*- coding: utf-8 -*-
from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_visually_sorted_moves(self):
        """
        Retorna las líneas de movimiento (move_ids_without_package) ordenadas
        por la ubicación física origen para optimizar la ruta de recolección en almacén.
        No modifica el orden en base de datos, solo para el reporte PDF.
        """
        self.ensure_one()
        return self.move_ids_without_package.sorted(
            key=lambda m: (m.location_id.complete_name or '', m.product_id.name or '')
        )

    def get_visually_sorted_move_lines(self):
        """
        Retorna las líneas de movimiento detalladas (move_line_ids_without_package) 
        ordenadas por la ubicación física origen para optimizar la recolección.
        No modifica el orden en base de datos, solo se utiliza en el reporte.
        """
        self.ensure_one()
        return self.move_line_ids_without_package.sorted(
            key=lambda ml: (ml.location_id.complete_name or '', ml.product_id.name or '')
        )

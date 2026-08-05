# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io

try:
    import openpyxl
except ImportError:
    openpyxl = None

class SmartExcelUpdate(models.TransientModel):
    _name = 'smart.excel.update'
    _description = 'Smart Excel Mass Update Wizard'

    state = fields.Selection([
        ('export', 'Export'),
        ('import', 'Import'),
        ('done', 'Done')
    ], string='Status', default='export')
    
    excel_file = fields.Binary('Excel File', attachment=False)
    file_name = fields.Char('File Name')
    log_message = fields.Text('Result Log', readonly=True)

    def action_generate_template(self):
        if not openpyxl:
            raise UserError(_("Please install the openpyxl python library to use this module."))
        
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError(_("No records selected. Please select products from the list view first."))
            
        products = self.env['product.template'].browse(active_ids)
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products Update"
        
        # Headers
        headers = ['ID (DO NOT MODIFY)', 'Internal Reference', 'Name', 'Sales Price', 'Cost']
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
        
        # Data
        for row_num, product in enumerate(products, 2):
            ws.cell(row=row_num, column=1, value=product.id)
            ws.cell(row=row_num, column=2, value=product.default_code or '')
            ws.cell(row=row_num, column=3, value=product.name or '')
            ws.cell(row=row_num, column=4, value=product.list_price or 0.0)
            ws.cell(row=row_num, column=5, value=product.standard_price or 0.0)
            
        # Save to BytesIO
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        file_data = base64.b64encode(output.read())
        self.write({
            'excel_file': file_data,
            'file_name': "Smart_Product_Update.xlsx",
            'state': 'import'
        })
        
        # Return action to trigger automatic browser download
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=smart.excel.update&id={self.id}&field=excel_file&filename=Smart_Product_Update.xlsx&download=true',
            'target': 'self',
        }
        
    def action_import_data(self):
        if not self.excel_file:
            raise UserError(_("Please upload an Excel file."))
            
        try:
            file_data = base64.b64decode(self.excel_file)
            input_stream = io.BytesIO(file_data)
            wb = openpyxl.load_workbook(input_stream, data_only=True)
            ws = wb.active
        except Exception as e:
            raise UserError(_("Invalid Excel file: %s") % str(e))
            
        success_count = 0
        errors = []
        
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
            if not row or not row[0]:
                continue
                
            try:
                prod_id = int(row[0])
                default_code = row[1] if row[1] is not None else ''
                name = row[2]
                list_price = float(row[3]) if row[3] is not None else 0.0
                standard_price = float(row[4]) if row[4] is not None else 0.0
                
                product = self.env['product.template'].browse(prod_id)
                if product.exists():
                    product.write({
                        'default_code': str(default_code) if default_code else False,
                        'name': str(name) if name else product.name,
                        'list_price': list_price,
                        'standard_price': standard_price
                    })
                    success_count += 1
                else:
                    errors.append(f"Row {row_idx}: Product ID {prod_id} not found in database.")
            except Exception as e:
                errors.append(f"Row {row_idx}: Ignored due to format error ({str(e)}).")
                
        log_msg = f"✅ Update Complete!\nSuccessfully updated: {success_count} products.\n"
        if errors:
            log_msg += "\n⚠️ Errors / Ignored Rows:\n" + "\n".join(errors)
            
        self.log_message = log_msg
        self.state = 'done'
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart.excel.update',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
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
    _description = 'Smart Excel Mass Update & Creation Wizard'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Completed')
    ], string='Status', default='draft')

    main_mode = fields.Selection([
        ('export', 'Export to Excel'),
        ('import', 'Import to Odoo')
    ], string='Operation', default='export', required=True)
    
    export_type = fields.Selection([
        ('update', 'Export currently selected products (for updating prices/data)'),
        ('blank', 'Download a blank template (for creating new products from scratch)')
    ], string='Export Option', default='update')
    
    exported_file = fields.Binary('Exported File', attachment=False)
    import_file = fields.Binary('Select Excel File', attachment=False)
    file_name = fields.Char('File Name')
    log_message = fields.Text('Result Log', readonly=True)

    def action_generate_template(self):
        if not openpyxl:
            raise UserError(_("Please install the openpyxl python library to use this module."))
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Products Data"
        
        headers = ['ID (Leave empty for new products)', 'Internal Reference', 'Barcode', 'Name', 'Sales Price', 'Cost', 'Weight (kg)']
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            
        if self.export_type == 'update':
            active_ids = self.env.context.get('active_ids', [])
            if not active_ids:
                raise UserError(_("No records selected. Please select products from the list view first before exporting."))
                
            products = self.env['product.template'].browse(active_ids)
            for row_num, product in enumerate(products, 2):
                ws.cell(row=row_num, column=1, value=product.id)
                ws.cell(row=row_num, column=2, value=product.default_code or '')
                ws.cell(row=row_num, column=3, value=product.barcode or '')
                ws.cell(row=row_num, column=4, value=product.name or '')
                ws.cell(row=row_num, column=5, value=product.list_price or 0.0)
                ws.cell(row=row_num, column=6, value=product.standard_price or 0.0)
                ws.cell(row=row_num, column=7, value=product.weight or 0.0)
            filename = "Exported_Products_Update.xlsx"
        else:
            ws.cell(row=2, column=1, value="")
            ws.cell(row=2, column=2, value="REF-001")
            ws.cell(row=2, column=3, value="1234567890123")
            ws.cell(row=2, column=4, value="Sample New Product")
            ws.cell(row=2, column=5, value=100.0)
            ws.cell(row=2, column=6, value=50.0)
            ws.cell(row=2, column=7, value=1.5)
            filename = "Blank_Product_Creation_Template.xlsx"
            
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        file_data = base64.b64encode(output.read())
        self.write({
            'exported_file': file_data,
            'file_name': filename,
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=smart.excel.update&id={self.id}&field=exported_file&filename={filename}&download=true',
            'target': 'self',
        }

    def action_import_data(self):
        if not self.import_file:
            raise UserError(_("Please select an Excel file from your computer before clicking Import."))
            
        try:
            file_data = base64.b64decode(self.import_file)
            input_stream = io.BytesIO(file_data)
            wb = openpyxl.load_workbook(input_stream, data_only=True)
            ws = wb.active
        except Exception as e:
            raise UserError(_("Invalid Excel file: %s") % str(e))
            
        updated_count = 0
        created_count = 0
        errors = []
        
        for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
            if not row or (row[0] is None and not any(row[1:])):
                continue
                
            try:
                raw_id = row[0]
                default_code = str(row[1]).strip() if row[1] is not None else False
                barcode = str(row[2]).strip() if row[2] is not None else False
                name = str(row[3]).strip() if row[3] is not None else False
                list_price = float(row[4]) if len(row) > 4 and row[4] is not None else 0.0
                standard_price = float(row[5]) if len(row) > 5 and row[5] is not None else 0.0
                weight = float(row[6]) if len(row) > 6 and row[6] is not None else 0.0
                
                vals = {}
                if default_code is not False: vals['default_code'] = default_code
                if barcode is not False: vals['barcode'] = barcode
                if name is not False: vals['name'] = name
                vals['list_price'] = list_price
                vals['standard_price'] = standard_price
                vals['weight'] = weight
                
                prod_id = None
                if raw_id is not None and str(raw_id).strip().isdigit():
                    prod_id = int(str(raw_id).strip())
                    
                if prod_id:
                    product = self.env['product.template'].browse(prod_id)
                    if product.exists():
                        product.write(vals)
                        updated_count += 1
                    else:
                        errors.append(f"Row {row_idx}: Product ID {prod_id} not found in Odoo database.")
                else:
                    if not name:
                        errors.append(f"Row {row_idx}: Skipped creating new product because 'Name' is empty.")
                    else:
                        self.env['product.template'].create(vals)
                        created_count += 1
            except Exception as e:
                errors.append(f"Row {row_idx}: Skipped due to error ({str(e)}).")
                
        log_msg = f"🎉 Process Finished Successfully!\n"
        log_msg += f"----------------------------------------\n"
        log_msg += f"✏️ Updated Existing Products: {updated_count}\n"
        log_msg += f"✨ Created New Products: {created_count}\n"
        
        if errors:
            log_msg += f"\n⚠️ Ignored Rows / Errors ({len(errors)}):\n" + "\n".join(errors)
            
        self.log_message = log_msg
        self.state = 'done'
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart.excel.update',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
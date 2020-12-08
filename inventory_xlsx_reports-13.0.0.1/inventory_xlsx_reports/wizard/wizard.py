from odoo import fields, models, api
from PIL import Image
from datetime import date
import io
import base64


class ModelName(models.TransientModel):
    _name = 'reports.xlsx'
    _description = 'Description'

    def _company_data(self):
        return self.env.user.company_id.id

    name = fields.Char()
    state = fields.Selection(
        [
            ('product', 'Product'),
            ('move', 'Moves'),
        ], required=True, default='product'
    )
    product_ids = fields.Many2many('product.product', required=True, )
    company_id = fields.Many2one('res.company', default=_company_data)

    @api.onchange('company_id')
    def onchange_method(self):
        users_groups = self.env.ref('base.group_multi_company')
        users = []
        for user in users_groups.users:
            users.append(user.id)
        if self.env.user.id in users:
            return {'domain': {'product_ids': [('company_id', '=', self.company_id.id)]}}

    def get_ids(self, type_ids):
        if type_ids in ['product', 'move']:
            return [val.id for val in self.product_ids]

    def get_print_data(self):
        # print("self.read()[0]", self.read()[0])
        data = {
            "name": self.name,
            "state": self.state
        }
        if self.state in ['product']:
            data['product'] = self.get_ids('product')
        if self.state in ['move']:
            data['move'] = self.get_ids('product')
        if self.company_id:
            data['company'] = self.company_id.id

        active_ids = self.env.context.get('active_ids', [])

        datas = {
            'ids': active_ids,
            'model': 'reports.xlsx',
            'data': data
        }
        return self.env.ref('inventory_xlsx_reports.inventory_def_reports_xlsx_id').report_action([], data=datas)


class PartnerXlsx(models.AbstractModel):
    _name = "report.inventory_xlsx_reports.inventory_def_reports_xlsx_id"
    _inherit = "report.report_xlsx.abstract"
    _description = "Inventory XLSX Report"

    def generate_xlsx_report(self, workbook, data, docs):
        print('generate_xlsx_report', data['data'], 'values', docs)
        heading = ['Name', 'Qty On Hand', 'Qty Purchase', 'Qty Sale', 'Forecasted', 'Total', 'Sales Price', 'Cost']
        if 'product' in data['data'].keys():
            # heading.append('Location')
            # heading.append('Warehouse')
            self.get_by_product(workbook, data, heading)
        if 'move' in data['data'].keys():
            self.get_move_details(workbook, data)

    def company_data(self, data=None):
        if 'company' in data['data'].keys():
            return self.env['res.company'].browse(int(data['data']['company']))
        return self.env.user.company_id

    def get_move_details(self, workbook, data):
        heading = ['Name', 'Date', 'Reference', 'Source', 'From', 'To', 'Quantity Done']
        sheet = workbook.add_worksheet(data['data']['name'])
        cell_format = workbook.add_format({'bold': True})
        cell_col_format = workbook.add_format()
        cell_col_format.set_fg_color('#ffffff')

        # =--------------name
        format_none = workbook.add_format()
        format_none.set_bg_color('#d2b48c')
        format_none.set_align('center')
        format_none.set_bold()
        # =--------------name
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_fg_color('#00e6e6')
        cell_format.set_pattern(1)
        sheet.set_column('A:A', 10, cell_col_format)
        # -------------company data
        format_company = workbook.add_format()
        format_company.set_align('center')
        format_company.set_align('vcenter')
        format_company.set_fg_color('#ffffff')
        format_company.set_font_name('Times New Roman')
        format_company.set_font_size(25)
        sheet.write(0, 4, self.company_data(data).name, format_company)
        sheet.write(2, 4, str('( ' + str(date.today()) + ' )'), format_company)
        sheet.write(1, 4, data['data']['name'], format_company)
        # print('---------', type(self.company_data().logo))
        buf_image = io.BytesIO(base64.b64decode(self.company_data(data).logo))
        # ,'x_offset': 0.5, 'y_offset': 0.5
        sheet.insert_image('G1', "data.png", {'x_scale': 0.15, 'y_scale': 0.1, 'image_data': buf_image})
        # --------------------data
        x = 7
        y = 1
        row_num_1 = 0
        count = 1
        sheet.set_row(x - 1, 40)
        sheet.write_row('B' + str(x), heading, cell_format)
        sheet.set_column('B:B', 35, cell_col_format)
        sheet.set_column('F:G', 35, cell_col_format)
        sheet.set_column('D:D', 30, cell_col_format)
        sheet.set_column('E:E', 25, cell_col_format)
        sheet.set_column('H:H', 15, cell_col_format)
        sheet.set_column('C:C', 20, cell_col_format)
        for products in data['data']['move']:
            new_row = 1
            product_ids = self.env['product.product'].browse(products)
            moves = self.env['stock.move.line'].search([('product_id', '=', products)])
            if moves:
                # sheet.write(x + row_num_1, 0, count,
                #             workbook.add_format({'align': 'center', 'bg_color': '#d2b48c'}))
                # count += 1
                sheet.write(x + row_num_1, 0 + y, product_ids.name + self.get_vale_product(
                    product_ids.product_template_attribute_value_ids) if
                product_ids.product_template_attribute_value_ids else
                product_ids.name, workbook.add_format(
                    {'bold': True, 'font_size': 10, 'align': 'center', 'bg_color': '#ffffff'}))
                # if product_ids.image_1920:
                # product_image = io.BytesIO(base64.b64decode(product_ids.image_1920))
                # # ,'x_offset': 0.5, 'y_offset': 0.5
                # sheet.insert_image('I'+str(x + row_num_1),
                # "data.png", {'x_scale': 0.15, 'y_scale': 0.1, 'image_data': product_image})
                for row_num_2, mov in enumerate(moves):
                    # sheet.write(x + row_num_1 + row_num_2, 0, count,
                    #             workbook.add_format({'align': 'center', 'bg_color': '#d2b48c'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 1 + y, mov.date,
                                workbook.add_format(
                                    {'num_format': 'mm/dd/yy', 'align': 'center', 'bg_color': '#DCDCDC'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 2 + y, mov.reference,
                                workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 3 + y, mov.origin if mov.origin else '',
                                workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 4 + y, mov.location_id.complete_name,
                                workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 5 + y, mov.location_dest_id.complete_name,
                                workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                    sheet.write(x + row_num_1 + row_num_2 + 1, 6 + y, mov.qty_done,
                                workbook.add_format({'align': 'center', 'bg_color': '#DCDCDC'}))
                    new_row += 1
                    # count += 1
                row_num_1 += new_row
        return sheet

    def get_by_product(self, workbook, data, headings):

        sheet = workbook.add_worksheet(data['data']['name'])
        cell_format = workbook.add_format({'bold': True})
        cell_col_format = workbook.add_format()
        cell_col_format.set_fg_color('#ffffff')
        format_none = workbook.add_format()
        # =--------------center

        # =--------------center
        format_none.set_bg_color('#d2b48c')
        format_none.set_align('center')
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_fg_color('#00e6e6')
        cell_format.set_pattern(1)
        sheet.set_column('A:A', 10, cell_col_format)
        # -------------company data
        format_company = workbook.add_format()
        format_company.set_align('center')
        format_company.set_align('vcenter')
        format_company.set_fg_color('#ffffff')
        format_company.set_font_name('Times New Roman')
        format_company.set_font_size(25)
        sheet.write(0, 4, self.company_data(data).name, format_company)
        sheet.write(2, 4, str('( ' + str(date.today()) + ' )'), format_company)
        sheet.write(1, 4, data['data']['name'], format_company)
        buf_image = io.BytesIO(base64.b64decode(self.company_data(data).logo))
        # ,'x_offset': 0.5, 'y_offset': 0.5
        sheet.insert_image('H1', "data.png", {'x_scale': 0.15, 'y_scale': 0.1, 'image_data': buf_image})
        # -------------company data
        x = 7
        y = 1
        sheet.set_row(x - 1, 40)
        sheet.write_row('B' + str(x), headings, cell_format)
        sheet.set_column('B:B', 35, cell_col_format)
        sheet.set_column('C:I', 15, cell_col_format)
        # sheet.set_column('J:K', 20, cell_col_format)
        # cell_format.set_border(6)
        col = 0
        row = 0
        product_ids = self.env['product.product'].browse(data['data']['product'])
        print('Length', len(product_ids))
        for row_num, data in enumerate(product_ids):
            if sum([data.qty_available, data.purchased_product_qty, data.sales_count]) <= 0:
                sheet.write(x + row_num, 0, row_num + 1,
                            workbook.add_format({'align': 'center', 'bg_color': '#d2b48c'}))
                sheet.write(x + row_num, 0 + y, data.name + self.get_vale_product(
                    data.product_template_attribute_value_ids) if data.product_template_attribute_value_ids else data.name,
                            format_none)
                sheet.write(x + row_num, 1 + y, data.qty_available, format_none)
                sheet.write(x + row_num, 2 + y, data.purchased_product_qty, format_none)
                sheet.write(x + row_num, 3 + y, data.sales_count, format_none)
                sheet.write(x + row_num, 4 + y, data.virtual_available, format_none)
                sheet.write(x + row_num, 5 + y, sum(
                    [data.qty_available, data.purchased_product_qty,
                     data.sales_count]) if data.qty_available else sum(
                    [data.virtual_available, data.purchased_product_qty, data.sales_count]),
                            format_none)
                sheet.write(x + row_num, 6 + y, data.lst_price, format_none)
                sheet.write(x + row_num, 7 + y, data.standard_price, format_none)

                # sheet.write(x + row_num, 8 + y, data.location_id.name if data.location_id else '', format_none)
                # sheet.write(x + row_num, 9 + y, data.warehouse_id.name if data.warehouse_id else '', format_none)
            else:
                sheet.write(x + row_num, 0, row_num + 1,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 0 + y, data.name,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 1 + y, data.qty_available,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 2 + y, data.purchased_product_qty,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 3 + y, data.sales_count,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 4 + y, data.virtual_available,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 5 + y, sum(
                    [data.qty_available, data.purchased_product_qty,
                     data.sales_count]) if data.qty_available else sum(
                    [data.virtual_available, data.purchased_product_qty, data.sales_count]),
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 6 + y, data.lst_price,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                sheet.write(x + row_num, 7 + y, data.standard_price,
                            workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                # sheet.write(x + row_num, 8 + y, data.location_id.name if data.location_id else '',
                #             workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
                # sheet.write(x + row_num, 9 + y, data.warehouse_id.name if data.warehouse_id else '',
                #             workbook.add_format({'align': 'center', 'bg_color': '#ffffff'}))
        return sheet

    def format_sheet(self, data, format_none):
        format_none.set_font_color('red')
        result = sum(data)
        return result if result != 0 else result, format_none

    def get_vale_product(self, values):
        name = ''
        for val in values:
            name += '/' + val.name
        return name

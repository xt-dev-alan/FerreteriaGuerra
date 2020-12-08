# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryXlsxReports(http.Controller):
#     @http.route('/inventory_xlsx_reports/inventory_xlsx_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_xlsx_reports/inventory_xlsx_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_xlsx_reports.listing', {
#             'root': '/inventory_xlsx_reports/inventory_xlsx_reports',
#             'objects': http.request.env['inventory_xlsx_reports.inventory_xlsx_reports'].search([]),
#         })

#     @http.route('/inventory_xlsx_reports/inventory_xlsx_reports/objects/<model("inventory_xlsx_reports.inventory_xlsx_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_xlsx_reports.object', {
#             'object': obj
#         })

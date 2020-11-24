# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS Sale order- Create Sales order from POS in Odoo",
    "version" : "13.0.0.1",
    "category" : "Point of Sale",
    "depends" : ['base','sale_management','point_of_sale'],
    "author": "BrowseInfo",
    'summary': 'Create Quotation from Point of Sale create sales from pos create sale order from point of sale Create Sale from POS Generate sales order from POS create SO from POS create sales from point of sales convert sales from pos create sales from pos sale order',
    "price": 25,
    "currency": 'EUR',
    "description": """
    
    Purpose :- 
    odoo Create Sales Order from Point of Sale create sale from POS
    odoo Create SO from POS Create sales from Point of Sale Add Quotation form POS Create Quotation from Point of Sales 
    odoo point of sales Create Sales from POS Generate sales order from POS Add Quotation from POS Create sales order from POS
    odoo Create Quotation Sale Order from Point of Sale Create Quotation from Point of Sale
    odoo Create Sale Order from Point of Sale sale order from POS
	odoo sale order of pos order create SO from POS order from POS
	
    odoo Create Sales Order from Point of Sale Create Sale from Point of Sale
    pos save quotation

odoo Create Sales Order from Point of Sale Create SO from POS Create sales from Point of Sales
        odoo Add Quotation form POS Create Quotation from Point of Sales
        odoo Create Sales from POS Generate sales order from POS
        odoo Add Quotatuon from POS Create sales order from POS

        odoo import Sales Order from Point of Sale import Sale from Point of Sale
        odoo import Sales from Point of Sale import SO from POS
        odoo Import SO from point of sale import sales from Point of Sale
        odoo Import sale order from POS import Quotation form POS
        odoo import Quotation from Point of Sales import Sales from POS
        odoo import sales order from POS import Quotatuon from POS, 
        odoo import sales order from POS odoo import quote from pos odoo import quote from point of sale
        odoo point of sale save quotation point of sale add quotation point of sale create quotation odoo
        odoo point of sales save quotation point of sales add quotation point of sales create quotation odoo
        odoo pos save quotation pos add quotation pos create quotation odoo
        This odoo apps helps to import order and import product from specific sale order or import whole sales order in point of sales system using POS touch screen. After installing this odoo modules you can see all the created quotation and sales order in pos screen using import order button you can easily import specific order as point of sales order. User will also have selection to choose which products and how much quantity of product they want to import on point of sale order.
    """,
    "website" : "https://www.browseinfo.in",
    'live_test_url':'https://youtu.be/2FlLTPsKonI',
    "data": [
        'views/custom_pos_view.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/pos_create_sales_order.xml',
    ],
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

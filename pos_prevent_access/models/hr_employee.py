# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    pos_discount_access = fields.Boolean(string="Access to Discount", default=True)
    pos_price_access = fields.Boolean(string="Access to Price", default=True)
    pos_negative_access = fields.Boolean(string="Access to +/-", default=True)

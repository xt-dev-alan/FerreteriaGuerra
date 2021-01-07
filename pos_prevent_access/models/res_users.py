# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_discount_access = fields.Boolean(string="Access to Discount", compute='_computePOSAccess')
    pos_price_access = fields.Boolean(string="Access to Price", compute='_computePOSAccess')
    pos_negative_access = fields.Boolean(string="Access to +/-", compute='_computePOSAccess')

    @api.depends('groups_id')
    def _computePOSAccess(self):
        for record in self:
            if record.has_group('pos_prevent_access.group_pos_discount_access'):
                record.pos_discount_access = True
            else:
                record.pos_discount_access = False
            if record.has_group('pos_prevent_access.group_pos_price_access'):
                record.pos_price_access = True
            else:
                record.pos_price_access = False
            if record.has_group('pos_prevent_access.group_pos_negative_access'):
                record.pos_negative_access = True
            else:
                record.pos_negative_access = False

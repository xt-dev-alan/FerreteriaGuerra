# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_access_level = fields.Boolean(string="POS Access on User Level", config_parameter='pos_prevent_access.pos_access_level')


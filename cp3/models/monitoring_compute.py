# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class MonitorngComputeDetail(models.Model):
    _name = 'monitoring.compute.detail'

    name = fields.Char(string="Name")
    value = fields.Float(string="Value", digits=(4, 5))
    compute_id = fields.Many2one('monitoring.devices', string="Compute")
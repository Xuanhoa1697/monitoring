# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitorngCompute(models.Model):
    _name = 'monitoring.compute'

    name = fields.Char(string="Name")
    code = fields.Text(string="Code", compute="_compute_code", store=True)
    alarm = fields.Float(string="Alarm")
    alert = fields.Float(string="Alert")
    warning = fields.Float(string="Warning")
    image = fields.Binary(string="Images")
    main_code = fields.Text(string="Main Code")
    compute_ids = fields.One2many('monitoring.compute.detail', 'compute_id', string="Compute")
    device_ids = fields.Many2many('monitoring.devices', 'device_compute_rel', string="Device")

    @api.depends('compute_ids')
    def _compute_code(self):
        for line in self:
            if line.compute_ids and line.code:
                for item in line.compute_ids:
                    if item.name in line.code:
                        if item.value and item.name:
                            line.code = line.code.replace(item.name, str(item.value))

class MonitorngComputeDetail(models.Model):
    _name = 'monitoring.compute.detail'

    name = fields.Char(string="Name")
    value = fields.Float(string="Value", digits=(4, 5))
    compute_id = fields.Many2one('monitoring.compute', string="Compute")
# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitoringDevices(models.Model):
    _name = 'monitoring.devices'

    name = fields.Char(string="Device")
    site_id = fields.Many2one('monitoring.sites', string="Station")
    type_id = fields.Many2one('monitoring.type', string="Type")
    description = fields.Text(string='Description')

    code = fields.Text(string="Code", compute= "_compute_code", store= True)
    alarm = fields.Float(string="Alarm")
    alert = fields.Float(string="Alert")
    warning = fields.Float(string="Warning")
    image = fields.Binary(string="Images")
    main_code = fields.Text(string="Main Code")
    compute_ids = fields.One2many('monitoring.compute.detail', 'compute_id', string="Compute")

    @api.depends('compute_ids')
    def _compute_code(self):
        for line in self:
            if line.compute_ids and line.main_code:
                if line.type_id.name == 'PZ':
                    line.code = line.main_code.replace('Ri', "{line.piezo_r}").replace('Ti', "{line.piezo_t}")
                for item in line.compute_ids:
                    if item.name in line.code:
                        if item.name:
                            line.code = line.code.replace(item.name, str(round(item.value, 4)))
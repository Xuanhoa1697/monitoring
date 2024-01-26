# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitoringDevices(models.Model):
    _name = 'monitoring.devices'

    name = fields.Char(string="Device")
    site_id = fields.Many2one('monitoring.sites', string="Station")
    type_id = fields.Many2one('monitoring.type', string="Type")
    description = fields.Text(string='Description')
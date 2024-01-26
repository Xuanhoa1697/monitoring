# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import os
global_path = 'D:\Web\TWGeology\monitoring_csv'


class MonitoringSites(models.Model):
    _name = 'monitoring.sites'

    name = fields.Char(string="Site Name")
    construction_id = fields.Many2one('construction.monitoring', string="Construction")
    path = fields.Char(string="Path")
    sites_manager = fields.Many2one('res.users', string="Construction Manager", related='construction_id.construction_manager')
    device_ids = fields.One2many('monitoring.devices','site_id', string="Devices")
    user_ids = fields.Many2many('res.users', 'monitoring_sites_user_rel', string="Worker")

    @api.model
    def create(self, vals):
        project = super(MonitoringSites, self).create(vals)
        if project.construction_id:
            file_patch = os.path.join(f'{global_path}\{project.construction_id.name}', project.name)
            print(file_patch)
            if not os.path.exists(file_patch):
                os.makedirs(file_patch)
                project.path = file_patch
        return project
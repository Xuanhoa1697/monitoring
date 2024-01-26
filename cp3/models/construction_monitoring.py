# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import os
global_path = 'D:\Web\TWGeology\monitoring_csv'

class ConstructionMonitoring(models.Model):
    _name = 'construction.monitoring'
    _order = "create_date desc"

    name = fields.Char(string="Construction Name")
    construction_manager = fields.Many2one('res.users', string="Construction Manager")
    construction_address = fields.Char(string="Construction Address")
    image = fields.Binary(string="Images")

    @api.model
    def create(self, vals):
        project = super(ConstructionMonitoring, self).create(vals)
        file_patch = os.path.join(global_path, project.name)
        print(file_patch)
        if not os.path.exists(file_patch):
            os.makedirs(file_patch)
        return project

    def write(self, vals):
        if vals.get('name'):
            file_patch = os.path.join(global_path, self.name)
            if os.path.exists(file_patch):
                new_path = os.path.join(global_path, vals.get('name'))
                os.rename(file_patch, new_path)
        res = super(ConstructionMonitoring, self).write(vals)
        return res
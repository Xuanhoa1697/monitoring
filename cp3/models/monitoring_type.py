# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitoringType(models.Model):
    _name = 'monitoring.type'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    csv_key_code = fields.Text(string="CSV Key Code")
    csv_row_code = fields.Text(string="CSV Row Code")
    excel_row_code = fields.Text(string="Excel Row Code")
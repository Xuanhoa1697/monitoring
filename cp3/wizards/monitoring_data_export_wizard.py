# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitoringDevices(models.TransientModel):
    _name = 'monitoring.data.wizard'

    date = fields.Date(string="Date", default=lambda self: fields.Date.context_today(self))
    construction_id = fields.Many2one('construction.monitoring', string="Construction", tracking=True)

    def export_data(self):
        self.ensure_one()
        input_args = {
            'date': self.date.strftime('%Y-%m-%d'),
            'construction_id': self.construction_id.id
        }
        return (
            self.env["ir.actions.report"]
            .search([("report_name", "=", 'cp3.monitoring_data_report_xlsx'), ("report_type", "=", 'xlsx')], limit=1)
            .report_action(self, data=input_args)
        )
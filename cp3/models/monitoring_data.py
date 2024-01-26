# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
import csv
import os
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
a

class MonitoringData(models.Model):
    _name = 'monitoring.data'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date desc"

    name = fields.Char(string="Devices Name", tracking=True)
    site_id = fields.Many2one('monitoring.sites', string="Site")
    device_id = fields.Many2one('monitoring.devices', string="Devices", tracking=True)
    construction_id = fields.Many2one('construction.monitoring', string="Construction", tracking=True)
    user_id = fields.Many2one('res.users', string="Create By", tracking=True)
    date = fields.Date(string="Date", tracking=True)
    location = fields.Char(string="Location", compute="_compute_location")
    chartjs = fields.Char(string="ChartJS")
    chart_code = fields.Char(string="Chart Code")
    code = fields.Char(string="Code", compute="_compute_code", store=True)
    description = fields.Char(string="Description")
    data_ids = fields.One2many('monitoring.data.detail','data_id', string="Data", tracking=True)

    @api.depends("device_id")
    def _compute_code(self):
        for item in self:
            item.code = item.device_id.type_id.code

    @api.onchange('site_id')
    def _onchange_site_id(self):
        self.construction_id = self.site_id.construction_id

    def _compute_location(self):
        location = ''
        if self.data_ids:
            location = str(self.data_ids[-1].latitude) + ',' + str(self.data_ids[-1].longitude)
        self.location = location

    def convert_to_csv(self, datas_ids):
        try:
            folder = self.site_id.path
            file_name = f'{self.name}-reading.csv'
            file_patch = os.path.join(folder, file_name)

            if not os.path.exists(file_patch):
                list_key = self.device_id.type_id.csv_key_code.split(",")
                init_data = [
                    ["Name", self.name],
                    ["Construct Name", self.construction_id.name],
                    ["Site Name", self.site_id.name],
                    ["Created date", self.date],
                    list_key
                ]
                self.csv_save_data("w", file_patch, init_data)
            for line in datas_ids:
                data = line.data_id.device_id.type_id.csv_row_code.format(line=line, \
                                last_update=(line.last_update + timedelta(hours=7)))
                self.csv_save_data("a", file_patch, data)
        except ValueError as e:
            print(e)
            pass

    def csv_save_data(self, event, file_patch, data):
        csv_data = []
        if event == 'a':
            for item in data.split(","):
                try:
                    float(item)
                    csv_data.append(float(item))
                except ValueError:
                    csv_data.append(item)
                    pass
            csv_data = [csv_data]
        else:
            csv_data = data
        try:
            with open(file_patch, event, newline='') as file_csv:
                writer = csv.writer(file_csv, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerows(csv_data)
        except ValueError as e:
            print(e)
            pass

    def compute_result(self):
        for rec in self.data_ids.sudo():
            rec.result = False
            if rec.data_id.device_id:
                compute = self.env['monitoring.compute'].sudo().search([('device_ids', 'in', rec.data_id.device_id.id)])
                if compute and compute.code:
                    try:
                        rec.result = float(eval(compute.code.format(line=rec)))
                    except ValueError as e:
                        pass
                        print(e)

    @api.model
    def get_datas(self, res_id):
        data = self.sudo().browse(res_id)
        dataset = []
        key = []
        warning = []
        alarm = []
        alert = []
        list_data = self.sudo().search([('device_id', '=', data.device_id.id), ('site_id', '=', data.site_id.id)])
        if data.device_id.type_id.code == 'PZ':
            for line in list_data:
                if line.data_ids:
                    dataset.insert(0, float(line.data_ids[-1].result))
                    key.insert(0,line.date)
                    compute = self.env['monitoring.compute'].sudo().search(
                        [('device_ids', 'in', line.device_id.id)])
                    warning.insert(0, float(compute.warning))
                    alarm.insert(0, float(compute.alarm))
                    alert.insert(0, float(compute.alert))
        return {
            'dataset': dataset,
            'key': key,
            'warning': warning,
            'alarm': alarm,
            'alert': alert,
            'name': data.device_id.name
        }

class MonitoringXslx(models.AbstractModel):
    _name = "report.cp3.monitoring_data_report_xlsx"
    _description = "Monitoring XLSX"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objects):
        data_ids = self.env['monitoring.data'].sudo().read_group(
                    domain=[('date', '=', data['date']), ('construction_id', '=', data['construction_id'])],
                    fields=['id', 'name'], groupby=['site_id']
                )
        if not data_ids:
            raise ValidationError('Can not find data with date %s' % data['date'])
        for line in data_ids:
            stt = 0
            current_row = 0
            site_id = self.env['monitoring.sites'].sudo().browse(line.get('site_id')[0])
            data = self.env['monitoring.data'].sudo().read_group(
                    domain=line.get('__domain'),
                    fields=['id', 'name'], groupby=['code'])
            sheet = workbook.add_worksheet(site_id.name)
            sheet.set_column(0, 0, 20)
            sheet.set_column(0, 1, 10)
            sheet.set_column(0, 2, 10)
            sheet.set_column(0, 3, 10)
            sheet.set_column(0, 4, 10)
            sheet.set_column(0, 5, 10)
            sheet.set_column(0, 6, 10)
            sheet.set_column(0, 7, 10)
            bold = workbook.add_format({"bold": True})
            for rec in data:
                device_code = rec.get('code')
                data_detail = self.env['monitoring.data'].search(rec.get('__domain'))
                stt += 1
                sheet.write(current_row + stt, 0, device_code, bold)
                for datas in data_detail:
                    stt += 1
                    row_index = 0
                    sheet.write(current_row + stt, 0, datas.name)
                    if datas.device_id.type_id.excel_row_code:
                        try:
                            data_ct = datas.device_id.type_id.excel_row_code.format(line=datas.data_ids[-1])
                            data_split = data_ct.split(",")
                            print(data_split)
                            for i in data_split:
                                row_index += 1
                                sheet.write(current_row + stt, row_index, i, bold)
                        except ValueError as e:
                            pass
                            print(e)
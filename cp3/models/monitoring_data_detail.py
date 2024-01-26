# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class MonitoringSites(models.Model):
    _name = 'monitoring.data.detail'

    #Piezo
    piezo_r = fields.Char(string="R")
    piezo_t = fields.Char(string="T")
    casa = fields.Char(string="Casa")

    #EX, CM
    ex_cm_r = fields.Char(string="R")
    ex_cm_t = fields.Char(string="T")

    #Crack Gauge
    cg_r = fields.Char(string="R")
    cg_latest = fields.Char(string="CG Latest")

    #MPX
    n1 = fields.Char(string="N1")
    n2 = fields.Char(string="N2")
    n3 = fields.Char(string="N3")
    n4 = fields.Char(string="N4")

    #TP
    TP_A_0 = fields.Char(string="A+")
    TP_A_180 = fields.Char(string="A-")

    note = fields.Char(string="Note")
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    result = fields.Char(string="Result")
    user_id = fields.Many2one('res.users', string="Last Update By")
    last_update = fields.Datetime(string="Last Update")
    data_id = fields.Many2one('monitoring.data', string="Data")
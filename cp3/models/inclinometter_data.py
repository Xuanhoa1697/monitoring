# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class Inclinometer(models.Model):
    _name = 'inclinometter.file'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "create_date desc"

    name = fields.Char(string="Inclinometer")
    user_id = fields.Many2one('res.users', string="Create By", \
                              default=lambda self: self.env.user, \
                              tracking=True)
    construction_id = fields.Many2one('construction.monitoring', string="Construction", tracking=True)
    site_id = fields.Many2one('monitoring.sites', string="Site")
    attachment_ids = fields.Many2many(
        'ir.attachment', 'inclinometer_ir_attachments_rel', \
        string='Attachments')

    @api.model
    def default_get(self, fields_list):
        res = super(Inclinometer, self).default_get(fields_list)
        res['name'] = f'INCL/{fields.Date.today().strftime("%d-%m-%Y")}'
        return res

    @api.model
    def create(self, vals):
        templates = super(Inclinometer, self).create(vals)
        for template in templates:
            if template.attachment_ids:
                template.attachment_ids.write({'res_model': self._name, 'res_id': template.id})
        return templates
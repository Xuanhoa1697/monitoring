from odoo import _, api, fields, models

class PinPosSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pin_manager = fields.Integer(string="PIN Manager", help="PIN Manager")

    @api.model
    def get_values(self):
        res = super(PinPosSettings, self).get_values()
        ifcSudo = self.env["ir.config_parameter"].sudo()
        pin_manager = ifcSudo.get_param("pin_of_pos.pin_manager", default="")

        res.update(
            pin_manager=pin_manager
        )
        return res

    def set_values(self):
        super(PinPosSettings, self).set_values()
        ICPSudo = self.env["ir.config_parameter"].sudo()
        ICPSudo.set_param("pin_of_pos.pin_manager", self.pin_manager or "")

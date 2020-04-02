from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError


class CrmCustomerInherit (models.Model):
    _inherit = "res.partner"
    related_patient_id = fields.Many2one("hms.patient")

    @api.constrains('email')
    def check_email(self):
        patients = self.env["hms.patient"].search([("email", "=", self.email)])
        if patients :
            raise ValidationError('Customer email cannot be the same as patient email')

    @api.multi
    def unlink(self):
        for record in self:
            if record.related_patient_id.id != False:
                raise UserError(f"You can't delete customer with patient related to him")
        super().unlink()

from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError



class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = "first_name"
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float(required=True)
    blood_type = fields.Selection(
        [
            ('A+', 'A+ve'),
            ('B+', 'B+ve'),
            ('O+', 'O+ve'),
            ('AB+', 'AB+ve'),
            ('A-', 'A-ve'),
            ('B-', 'B-ve'),
            ('O-', 'O-ve'),
            ('AB-', 'AB-ve')
        ]
    )
    pcr = fields.Boolean()
    image = fields.Binary(string='Image')
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    department_id = fields.Many2one(comodel_name="hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctors_ids = fields.Many2many(comodel_name="hms.doctor")
    state = fields.Selection(
        [
            ('Undetermined', 'Undetermined'),
            ('Good', 'Good'),
            ('Fair', 'Fair'),
            ('Serious', 'Serious')
        ]
    )
    log_ids = fields.One2many('patient.log2', 'patient_id')
    email = fields.Text(required=True)
    _sql_constraints = [('validate_email_unique', 'unique(email)', 'Email already exists.')]

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "Warning",
                    'message': "PCR has been checked"
                }
            }

    def change_patient_state(self, vals):
        self.state = vals['state']

    @api.multi
    def write(self, vals):
        if 'state' in vals:
            print("yes")
            self.env["patient.log2"].create([
                {'description': f"Changed status to {vals['state']}",
                 'patient_id': self.id
                }
            ])
            new_record = super(HmsPatient, self).write(vals)

        else:
            new_record = super(HmsPatient, self).write(vals)
        return new_record

    @api.constrains('email')
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.match(regex, self.email) is None:
            raise ValidationError('Invalid Email')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            today = date.today()
            record.age = today.year - record.birth_date.year -\
                  ((today.month, today.day) <
             (record.birth_date.month, record.birth_date.day))



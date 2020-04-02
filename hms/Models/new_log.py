from odoo import models, fields, api
from datetime import datetime

class PatientLog2 (models.Model):
    _name = 'patient.log2'
    _rec_name = "create_uid"
    description = fields.Text()
    patient_id = fields.Many2one(comodel_name="hms.patient")




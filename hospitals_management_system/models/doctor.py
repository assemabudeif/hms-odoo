from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hms.doctor'

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patient_ids = fields.One2many('hms.patient', 'doctor_id')

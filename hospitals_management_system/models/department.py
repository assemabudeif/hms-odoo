
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'hms.department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id')
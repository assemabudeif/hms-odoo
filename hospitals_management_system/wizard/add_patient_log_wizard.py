from odoo import models, fields


class AddPatientLog(models.TransientModel):
    _name = 'hms.add.patient.log'

    patient_log_id = fields.Many2one('hms.patient.log')
    created_by = fields.Many2one('hms.doctor')
    date = fields.Datetime(default=fields.Date.today())
    description = fields.Text(string='Description')

    def action_add_patient_log(self):
        self.ensure_one()
        self.patient_log_id.description = self.description

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat = fields.Char(string='Tax ID', required=True)

    @api.constrains('email')
    def _check_email_unique_across_models(self):
        for rec in self:
            if rec.email:
                patient_with_email = self.env['hms.patient'].search([('email', '=', rec.email)], limit=1)
                if patient_with_email:
                    raise ValidationError('The email %s is already used by a patient rec.' % rec.email)

    def unlink(self):
        for rec in self:
            patient_linked = self.env['hms.patient'].search([('id', '=', rec.related_patient_id.id)], limit=1)
            if patient_linked:
                raise ValidationError('You cannot delete this customer because it is linked to a patient.')
        return super(ResPartner, self).unlink()

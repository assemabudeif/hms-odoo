from email.policy import default

from dateutil.relativedelta import relativedelta
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a-', 'A-'),
        ('a+', 'A+'),
        ('o-', 'O-'),
        ('o+', 'O+'),
        ('b-', 'B-'),
        ('b+', 'B+'),
        ('ab-', 'AB-'),
        ('ab+', 'AB+'),
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')
    department_id = fields.Many2one('hms.department', domain=[('is_opened', '=', True)], )
    doctor_id = fields.Many2many('hms.doctor')
    department_capacity = fields.Integer(
        compute='_compute_department_capacity',
        store=True
    )
    log_ids = fields.One2many('hms.patient.log', 'patient_id')
    state = fields.Selection(
        [
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious')
        ],
        default='undetermined',
        required=True,
    )
    show_log_history = fields.Boolean(compute='_compute_show_log_history')
    email = fields.Char(string='Email', required=True, unique=True)

    @api.constrains('email')
    def _check_valid_email(self):
        email_validate_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        for rec in self:
            if rec.email:
                if not re.match(email_validate_pattern, rec.email):
                    raise ValidationError('Invalid email address: %s' % rec.email)

    @api.depends('age')
    def _compute_show_log_history(self):
        for rec in self:
            rec.show_log_history = rec.age >= 50

    @api.depends('department_id')
    def _compute_department_capacity(self):
        for rec in self:
            if rec.department_id:
                rec.department_capacity = rec.department_id.capacity
            else:
                rec.department_capacity = 0

    @api.onchange('department_id')
    def _onchange_department(self):
        if not self.department_id:
            self.doctor_id = False

    @api.onchange('pcr')
    def _onchange_pcr(self):
        """Make CR Ratio mandatory if PCR is checked."""
        if self.pcr and not self.cr_ratio:
            return {
                'warning': {
                    'title': 'CR Ratio Required',
                    'message': 'CR Ratio is mandatory when PCR is checked.',
                }
            }

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0

    @api.onchange('state')
    def _onchange_state(self):
        for rec in self:
            if rec.state:
                rec.log_ids.create({
                    'description': f"State changed to {self.state.capitalize()}",
                })

    @api.onchange('age')
    def _onchange_age(self):
        for rec in self:
            if rec.age < 30:
                rec.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Checked Automatically',
                        'message': 'The PCR field has been checked automatically because the age is less than 30.',
                    }
                }

    def action_undetermined(self):
        for rec in self:
            rec.state = 'undetermined'

    def action_good(self):
        for rec in self:
            rec.state = 'good'

    def action_fair(self):
        for rec in self:
            rec.state = 'fair'

    def action_serious(self):
        for rec in self:
            rec.state = 'serious'

    def action_add_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('hospitals_management_system.patient_log_wizard_action')
        action['context'] = {
            'created_by': self.id
        }
        return action


class PatientLog(models.Model):
    _name = 'hms.patient.log'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Many2one('hms.doctor')
    date = fields.Datetime(default=fields.Date.today())
    description = fields.Text(string='Description')

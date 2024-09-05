from odoo import models, fields


class Ticket(models.Model):
    _name = 'todo.ticket'

    name = fields.Char()
    number = fields.Char()
    tag = fields.Char()
    description = fields.Char()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ])
    file = fields.Binary()

    def action_new(self):
        for rec in self:
            rec.state =  'new'


    def action_doing(self):
        for rec in self:
            rec.state = 'doing'


    def action_done(self):
        for rec in self:
            rec.state = 'done'



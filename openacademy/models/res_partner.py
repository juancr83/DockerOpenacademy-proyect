# -*- coding: utf-8 -*-

from openerp import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(default=False,help="This partner give train our course")
    sessions = fields.Many2many('session', string="Session as atendes", readonly=True)



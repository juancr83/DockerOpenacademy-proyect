# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Course(models.Model):
    _name = 'course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Descripcion')
    responsible = fields.Many2one('res.users',
				ondelete='set null',
				string="Responsible", index=True)
    sessions = fields.One2many('session','course')

class Session(models.Model):
    _name = 'session'

    name = fields.Char()
    instructor = fields.Many2one('res.partner',string="Instructor", 
                        domain=['|',
                                ("instructor","=",True),
                                ("category_id.name","ilike","Teacher")
                         ]
                        )
    course = fields.Many2one('course')
    start_date = fields.Date()
    duration = fields.Float(help="Duration in Days")
    seats = fields.Integer()
    attendees = fields.Many2many('res.partner', string="Attendees")
    percentage_seats_taken = fields.Float(compute="_compute_perc_seats_taken", store=True)


    @api.depends('attendees','seats')
    def _compute_perc_seats_taken(self):
        for record in self:
            if record.seats:
                record.percentage_seats_taken = float(len(record.attendees)) / record.seats * 100.00 
            else:
                record.percentage_seats_taken = 0.00



# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

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
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(help="Duration in Days")
    seats = fields.Integer()
    attendees = fields.Many2many('res.partner', string="Attendees")
    percentage_seats_taken = fields.Float(compute="_compute_perc_seats_taken", store=True)
    active = fields.Boolean(default=True)


    @api.depends('attendees','seats')
    def _compute_perc_seats_taken(self):
        for record in self:
            if record.seats:
                record.percentage_seats_taken = float(len(record.attendees)) / record.seats * 100.00 
            else:
                record.percentage_seats_taken = 0.00

    @api.onchange('seats', 'attendees')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendees):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.one
    @api.constrains('instructor', 'attendees')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor and r.instructor in r.attendees:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

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

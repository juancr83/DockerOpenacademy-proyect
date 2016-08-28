# -*- coding: utf-8 -*-

from datetime import timedelta
from openerp import models, fields, api, exceptions

class Course(models.Model):
    _name = 'course'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Descripcion')
    responsible = fields.Many2one('res.users',
				ondelete='set null',
				string="Responsible", index=True)
    sessions = fields.One2many('session','course')

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

    @api.one
    def copy(self, default=None):
#        print "Estoy haciendo una prueba ****************************"
#        default['name'] = self.name + ' (copy)'
        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

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
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    color = fields.Integer()
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ], default='draft')
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('attendees')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendees)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

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

    @api.one
    @api.depends('duration', 'start_date')
    def _get_end_date(self):
        print "_get end date +++++++++++++++++++++++++++++" 
        if not (self.start_date and self.duration):
            self.end_date = self.start_date
            return
        start = fields.Datetime.from_string(self.start_date)
        duration = timedelta(days=self.duration, seconds=-1)
        self.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            print "_set end date ----------------------------"
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = fields.Datetime.from_string(r.start_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1 

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

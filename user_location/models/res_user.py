# -*- coding: utf-8 -*-


#from msilib.schema import Class
from odoo import api, fields, models
import requests
from geopy.geocoders import Nominatim
from odoo.exceptions import UserError, ValidationError


class Users(models.Model):

    _inherit = 'res.users'


class Timesheet(models.Model):
    _inherit = "project.task"
    current_loc = fields.Char()

    def action_timer_start(self):
        self.current_loc = False

        valss = {}
       # url = 'http://ipinfo.io/json'
        url = 'https://ipinfo.io/json'

        r = requests.get(url)
        js = r.json()
        loc = js['loc']
        longi = loc.split(',')[1]
        latti = loc.split(',')[0]
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(loc)
        ans = location
        self.current_loc = ans
        res = super(Timesheet, self).action_timer_start()
        return res

#     def save_timesheet(self):


#         values = {
#             'task_id': self.task_id.id,
#             'project_id': self.task_id.project_id.id,
#             'date': fields.Date.context_today(self),
#             'name': self.description,
#             'user_id': self.env.uid,
#             'unit_amount': self.task_id._get_rounded_hours(self.time_spent * 60),
#         }
#         self.task_id.user_timer_id.unlink()
#         return self.env['account.analytic.line'].create(values)

# class Users(models.Model):
#     _inherit = 'account.analytic.line'

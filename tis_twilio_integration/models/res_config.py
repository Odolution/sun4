# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from twilio.rest import Client
import requests
import json


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    twilio_phone_no = fields.Char(string='Twilio Phone Number')
    twilio_account_sid = fields.Char(string='Twilio Account SID')
    twilio_auth_token = fields.Char(string='Twilio Auth Token')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('twilio_phone_no', self.twilio_phone_no)
        set_param('twilio_account_sid', self.twilio_account_sid)
        set_param('twilio_auth_token', self.twilio_auth_token)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            twilio_phone_no=get_param('twilio_phone_no', default=''),
            twilio_account_sid=get_param('twilio_account_sid', default=''),
            twilio_auth_token=get_param('twilio_auth_token', default=''),
        )
        return res

    def get_twilio_api_credentials(self):
        url_action = {
            'type': 'ir.actions.act_url',
            'name': "Twilio API Credentials",
            'target': 'new',
            'url': 'https://www.twilio.com/console',
        }
        return url_action

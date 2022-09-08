# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.


from odoo import models, fields


class SmsContactList(models.Model):
    _name = "sms.contact.list"
    _description = 'Twilio SMS Contact List'

    name = fields.Char(string='List Name', required=True)
    members_ids = fields.Many2many('res.partner', string='Members')

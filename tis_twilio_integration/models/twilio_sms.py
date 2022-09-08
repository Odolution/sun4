# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class TwilioSMSBase(models.Model):
    _name = "twilio.sms.base"
    _description = 'Twilio SMS Base'

    name = fields.Char(string='Subject', required=True)
    recipient_type = fields.Selection([
        ('individual', 'Individual Member'),
        ('multiple', 'Multiple Member'),
        ('contact_list', 'Contact Lists')], string="Recipient Types", required=True, default='individual')
    individual_member_id = fields.Many2one('res.partner', string="Select Member")
    multiple_member_ids = fields.Many2many('res.partner', string="Select Members")
    contact_list_ids = fields.Many2many('sms.contact.list', string="Contact Lists")
    body = fields.Text('Message', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
    ], string="State", required=True, default='draft')
    success_count = fields.Integer(string='Sent')
    bounce_count = fields.Integer(string='Bounce')
    success_partner_ids = fields.Many2many(relation='success_partner_rel', comodel_name='res.partner',
                                           string="Success Partners")
    failed_partner_ids = fields.Many2many(relation='failed_partner_rel', comodel_name='res.partner',
                                          string="Failed Partners")

    def action_send_twilio_sms(self):
        for rec in self:
            success_list = []
            success_partner_list = []
            bounce_list = []
            bounce_partner_list = []
            twilio_phone_no = self.env['ir.config_parameter'].sudo().get_param('twilio_phone_no')
            twilio_account_sid = self.env['ir.config_parameter'].sudo().get_param('twilio_account_sid')
            twilio_auth_token = self.env['ir.config_parameter'].sudo().get_param('twilio_auth_token')
            message_id = self.env['message.wizard']
            if twilio_account_sid and twilio_auth_token and twilio_phone_no:
                client = Client(twilio_account_sid, twilio_auth_token)
                if rec.recipient_type == 'individual':
                    try:
                        message = client.messages.create(
                            body=rec.body,
                            from_=twilio_phone_no,
                            to=rec.individual_member_id.mobile,
                        )
                    except Exception as e:
                        raise UserError(_(e.args[2]))
                    if message.status == 'queued':
                        success_list.append(rec.individual_member_id.name)
                        success_partner_list.append(rec.individual_member_id.id)
                    if message.status != 'queued':
                        bounce_list.append(rec.individual_member_id.name)
                        bounce_partner_list.append(rec.individual_member_id.id)
                if rec.recipient_type == 'multiple':
                    for member in rec.multiple_member_ids:
                        try:
                            message = client.messages.create(
                                body=rec.body,
                                from_=twilio_phone_no,
                                to=member.mobile,
                            )
                        except Exception as e:
                            raise UserError(_(e.args[2]))
                        if message.status == 'queued':
                            success_list.append(member.name)
                            success_partner_list.append(member.id)
                        if message.status == 'failed':
                            bounce_list.append(member.name)
                            bounce_partner_list.append(member.id)
                if rec.recipient_type == 'contact_list':
                    for contact_list in rec.contact_list_ids:
                        for member in contact_list.members_ids:
                            try:
                                message = client.messages.create(
                                    body=rec.body,
                                    from_=twilio_phone_no,
                                    to=member.mobile,
                                )
                            except Exception as e:
                                raise UserError(_(e.args[2]))
                            if message.status == 'queued':
                                success_list.append(member.name)
                                success_partner_list.append(member.id)
                            if message.status == 'failed':
                                bounce_list.append(member.name)
                                bounce_partner_list.append(member.id)
                rec.success_count = len(success_list)
                rec.bounce_count = len(bounce_list)
                rec.state = 'sent'
                rec.success_partner_ids = [(6, 0, success_partner_list)]
                rec.failed_partner_ids = [(6, 0, bounce_partner_list)]
                success_string = ','.join(map(str, success_list))
                bounce_string = ','.join(map(str, bounce_list))
                if success_list and bounce_list:
                    message_id = self.env['message.wizard'].create(
                        {'success_message': _("Message sent successfully to " + success_string),
                         'bounce_message': _(
                             "Message failed to sent for: " + bounce_string),
                         's_flag': True,
                         'b_flag': True,
                         })
                elif success_list and not bounce_list:
                    message_id = self.env['message.wizard'].create(
                        {'success_message': _("Message sent successfully to " + success_string),
                         's_flag': True})
                elif not success_list and bounce_list:
                    message_id = self.env['message.wizard'].create(
                        {'bounce_message': _("Message failed to sent for " + bounce_string),
                         'b_flag': True})
                return {
                    'name': _('Response'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    'res_id': message_id.id,
                    'target': 'new'
                }
            else:
                raise UserError(_('Please configure the API credentials in Settings.'))

    def action_view_success_partner(self):
        self.ensure_one()
        partner_list = []
        action = self.env.ref('contacts.action_contacts').read()[0]
        for partner in self.success_partner_ids:
            partner_list.append(partner.id)
        action['domain'] = [('id', 'in', partner_list)]
        return action

    def action_view_failed_partner(self):
        self.ensure_one()
        partner_list = []
        action = self.env.ref('contacts.action_contacts').read()[0]
        for partner in self.failed_partner_ids:
            partner_list.append(partner.id)
        action['domain'] = [('id', 'in', partner_list)]
        return action

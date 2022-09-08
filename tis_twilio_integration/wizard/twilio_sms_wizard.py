# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2019. All rights reserved.


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from twilio.rest import Client


class TwilioSMSWizard(models.TransientModel):
    _name = 'twilio.sms.wizard'
    _description = 'Twilio Send SMS Wizard'

    body = fields.Text('Message', required=True)
    partner_ids = fields.Many2many('res.partner', string='Recipients', readonly=True)

    def send_twilio_sms(self):
        sucess_list = []
        bounce_list = []
        partner = self.env['res.partner'].search([('id', 'in', self._context.get('active_ids'))])
        self.partner_ids = [(6, 0, self._context.get('active_ids'))]
        twilio_phone_no = self.env['ir.config_parameter'].sudo().get_param('twilio_phone_no')
        twilio_account_sid = self.env['ir.config_parameter'].sudo().get_param('twilio_account_sid')
        twilio_auth_token = self.env['ir.config_parameter'].sudo().get_param('twilio_auth_token')
        if twilio_account_sid and twilio_auth_token and twilio_phone_no:
            client = Client(twilio_account_sid, twilio_auth_token)
            for partner in self.partner_ids:
                try:
                    message = client.messages.create(
                        body=self.body,
                        from_=twilio_phone_no,
                        to=partner.mobile,
                    )
                except Exception as e:
                    raise UserError(_(e.args[2]))
                if message.status == 'queued':
                    sucess_list.append(partner.name)
                if message.status == 'failed':
                    bounce_list.append(partner.name)
            succes_string = ','.join(map(str, sucess_list))
            bounce_string = ','.join(map(str, bounce_list))
            if sucess_list and bounce_list:
                message_id = self.env['message.wizard'].create(
                    {'success_message': _("Message sent successfully to " + succes_string),
                     'bounce_message': _(
                         "Message failed to sent for: " + bounce_string),
                     's_flag': True,
                     'b_flag': True,
                     })
            elif sucess_list and not bounce_list:
                message_id = self.env['message.wizard'].create(
                    {'success_message': _("Message sent successfully to " + succes_string),
                     's_flag': True})
            elif not sucess_list and bounce_list:
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

# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_send_sms(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Send SMS Via Twilio'),
                'res_model': 'twilio.sms.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_ids': [(6, 0, self.ids)]},
                }

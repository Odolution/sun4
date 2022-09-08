# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

from odoo import models, fields, api, _


class MessageWizard(models.TransientModel):
    _name = 'message.wizard'

    success_message = fields.Text(string='Success Message', readonly=True)
    bounce_message = fields.Text(string='Bounce Message', readonly=True)
    s_flag = fields.Boolean(string='Success', default=False)
    b_flag = fields.Boolean(string='Failed', default=False)

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}

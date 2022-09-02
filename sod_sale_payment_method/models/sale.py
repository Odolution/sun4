# Copyright 2019-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_method_id = fields.Char(
        string='Payment Method'
    )

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     res = super(SaleOrder, self).onchange_partner_id()
    #     if self.partner_id.commercial_partner_id.sale_payment_method_id:
    #         self.payment_method_id = self.partner_id.commercial_partner_id.sale_payment_method_id.id
    #     elif self.partner_id.sale_payment_method_id:
    #         self.payment_method_id = self.partner_id.sale_payment_method_id.id
    #     return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        #invoice_vals['payment_method_id_invc'] = self.payment_method_id.id
        invoice_vals['payment_method_id_invc'] = self.payment_method_id
        return invoice_vals

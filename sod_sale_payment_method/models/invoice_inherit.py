from odoo import models, api, fields, _


class SaleOrder(models.Model):
    _inherit = 'account.move'

    payment_method_id_invc = fields.Char(
        string='Payment Method',
    )

   # def _payment_method_sale(self):
    #   sale_payment_id=self.env['sale.order'].search([('id','=',self.sale_line_id.id)])

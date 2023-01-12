from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
from datetime import datetime,date

class inheritintimesheet(models.Model):
    _inherit = 'account.analytic.line'

class signaturedelivery(models.Model):
    _inherit = 'stock.picking'

    dispatcher_name = fields.Char(string='Name')
    installation_signature = fields.Binary(string='Signature')








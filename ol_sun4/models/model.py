from odoo import models, fields,api
from odoo.exceptions import UserError
import base64
import requests
from datetime import datetime,date

class inheritintimesheet(models.Model):
    _inherit = 'account.analytic.line'








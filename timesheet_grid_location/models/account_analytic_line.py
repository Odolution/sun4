from odoo import models, fields


class LongGeo(models.Model):
    _inherit='account.analytic.line'
    location = fields.Char(string='Location')

    def save_location(self,args):
        self.env['account.analytic.line'].search([('id','=',args['id'])]).write({
            'location':str("https://maps.google.com/?q="+str(args['latitude'])+',' + str(args['longitude'])),

        })
        return args
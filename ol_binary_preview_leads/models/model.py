
from odoo import models, api, fields, _
from odoo.exceptions import UserError




class ext(models.Model):
     _inherit = "crm.lead"
     def preview(self,field_name):
         return { 
                  'name'     : 'Go to website',
                  'res_model': 'ir.actions.act_url',
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'self',
                  'url'      : '/web/content/'+self._name+'/'+str(self.id)+'/'+field_name
               }
     def preview_Contract(self):
         return self.preview("x_studio_contract")
     def preview_Proposal(self):
         return self.preview("x_studio_proposal")
     def preview_Utility_bill(self):
         return self.preview("x_studio_utility_bill")
     sample_field = fields.Binary(string="Sample Attachment")
     def preview_sample_binary(self):
         return self.preview("sample_field")
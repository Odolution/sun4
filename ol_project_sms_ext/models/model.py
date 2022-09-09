
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class twillioSMSExt(models.Model):
    _inherit = 'twilio.sms.base'
    project_id = fields.Many2one('project.project', string='project_id')
class projectExt(models.Model):
    _inherit = 'project.project'
    
    draft_subject = fields.Char('Subject')
    draft_message = fields.Text('Body')
    messages_ids = fields.One2many('twilio.sms.base', 'project_id', string='messages')
    
    def action_send_sms(self):
        for rec in self:
            if (not rec.draftMessage) or rec.draftMessage=="":
                continue
            
            ids=[rec.partner_id.id]
            
            rec.env['twilio.sms.base'].create({
                'project_id':rec.id,
                'body':rec.draftMessage,
                'name':rec.draft_subject,
                'multiple_member_ids':[(6, 0, ids)],
            })
        return
    
        
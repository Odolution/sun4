
from odoo import models, api, fields, _
from odoo.exceptions import UserError


class twillioSMSExt(models.Model):
    _inherit = 'twilio.sms.base'
    sms_type = fields.Selection([('outgoing', 'Sent'),('incoming','Received')], string= 'Type')
    project_id = fields.Many2one('project.project', string='project_id')
    chatter_name = fields.Char(string='Chatter')
    
        
class projectExt(models.Model):
    _inherit = 'project.project'
    
    draft_subject = fields.Char('Subject')
    draft_message = fields.Text('Body')
    messages_ids = fields.One2many('twilio.sms.base', 'project_id', string='messages')
    
    def action_send_sms(self):
        for rec in self:
            if (not rec.draft_message) or rec.draft_message=="":
                continue
            if not rec.partner_id:
                raise UserError("Partner not selected.")
            sms=rec.env['twilio.sms.base'].create({
                'project_id':rec.id,
                'body':rec.draft_message,
                'name':rec.draft_subject,
                'sms_type':'outgoing',
                'chatter_name':"Me",
                'individual_member_id':rec.partner_id.id,
            })
            sms.action_send_twilio_sms()
            rec.draft_subject=""
            rec.draft_message=""
        return
    
        
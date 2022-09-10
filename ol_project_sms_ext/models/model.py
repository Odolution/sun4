
from odoo import models, api, fields, _
from odoo.exceptions import UserError
from twilio.rest import Client
from datetime import datetime
from pytz import timezone, UTC
class twillioSMSExt(models.Model):
    _inherit = 'twilio.sms.base'
    sms_type = fields.Selection([('outgoing', 'Sent'),('incoming','Received')], string= 'Type')
    project_id = fields.Many2one('project.project', string='project_id')
    chatter_name = fields.Char(string='Chatter Name')
    message_time = fields.Datetime('message_time')
    
    def _readMessages(self):
        twilio_phone_no=self.env['ir.config_parameter'].sudo().get_param('twilio_phone_no',default='')
        twilio_account_sid=self.env['ir.config_parameter'].sudo().get_param('twilio_account_sid',default='')
        twilio_auth_token=self.env['ir.config_parameter'].sudo().get_param('twilio_auth_token',default='')
        try:
            tz=timezone(self.env.user.tz)
        except:
            tz=timezone("Asia/Karachi")
        old_tz = timezone('UTC')
        
        client = Client(twilio_account_sid, twilio_auth_token)
        
        
        last_synced=self.read_last_synced()
        if last_synced:
            messages = client.messages.list(date_sent_after=last_synced)
        else:
            messages = client.messages.list()

        for record in messages:
            if str(record.from_)!=str(twilio_phone_no):
                partners=self.env['res.partner'].search(['|',('phone','=',record.from_),('mobile','=',record.from_)])
                partnerids=[i.id for i in partners]
                stages=self.env['project.project.stage'].search([('name','in',['Site Survey','Design','Permitting','Installation','Permission to Operate','Project On Hold'])])
                stage_ids=[i.id for i in stages]
                projects=self.env['project.project'].search(['|',('stage_id','in',stage_ids),('partner_id','in',partnerids)])
                if projects:
                    sms=self.env['twilio.sms.base'].create({
                        'project_id':projects[0].id,
                        'body':record.body,
                        'name':"incoming",
                        'sms_type':"incoming",
                        'state':'sent',
                        'chatter_name':projects[0].partner_id.name if projects[0].partner_id else "Them",
                        'individual_member_id':projects[0].partner_id.id,
                        
                    })
                elif partners:
                    sms=self.env['twilio.sms.base'].create({
                        'body':record.body,
                        'name':"incoming",
                        'sms_type':"incoming",
                        'state':'sent',
                        'chatter_name':partners[0].name if partners[0] else "Them",
                        'individual_member_id':partners[0].id,
                        
                    })
                local = record.date_created.astimezone(tz)
                message_time = datetime.datetime(local.year, local.month, local.day, local.hour, local.minute, local.second, local.microsecond)
                sms.message_time=message_time
        self.write_last_synced(datetime.now(tz=tz))
            
    def read_last_synced(self):
        vars=self.env['twilio.sms.cronevars']
        if len(vars)==0:
            return None
        return vars[0].last_synced
    def write_last_synced(self,last_synced):
        vars=self.env['twilio.sms.cronevars']
        if len(vars)==0:
            self.env['twilio.sms.cronevars'].create({'last_synced':last_synced})
            return
        var[0]=last_synced
        return

class twilioVars(models.Model):
    _name = "twilio.sms.cronevars"
    last_synced = fields.Datetime('last_synced')
        
class projectExt(models.Model):
    _inherit = 'project.project'
    
    draft_subject = fields.Char('Subject')
    draft_message = fields.Text('Body')
    messages_ids = fields.One2many('twilio.sms.base', 'project_id', string='messages')
    
    def action_send_sms(self):
        try:
            tz=timezone(self.env.user.tz)
        except:
            tz=timezone("Asia/Karachi")
            
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
                'message_time':datetime.now(tz=tz)
            })
            sms.action_send_twilio_sms()
            rec.draft_subject=""
            rec.draft_message=""
        return
    

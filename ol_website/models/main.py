from odoo import http
from odoo.http import request
from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import base64
import requests


class surveryform(http.Controller):

    @http.route('/Sun4PR', auth='public', website='True')
    def index(self):
        return request.render('ol_website.form_submission')


class visitorform(http.Controller):

    @http.route('/visitorform', auth='public', website='True', csrf=False)
    def index(self, **post):
        print(post.get('name'))
        print(post.get('address'))
        print(post.get('email'))
        print(post.get('phone'))
        request.session['name'] = post.get('name')
        request.session['address'] = post.get('address')
        request.session['email'] = post.get('email')
        request.session['phone'] = post.get('phone')
        # request.session['bill']


        if request.session['bill'] == 1:
            vari = '$100-$150'
        elif request.session['bill'] == 2:
            vari = '$100-$150'
        elif request.session['bill'] == 3:
            vari = '$100-$150'
        else:
            vari = '$300+'


        lead = {
            'name': post.get('name'),
            'email_from': post.get('email'),
            'phone': post.get('phone'),
            'description': "Address is" + " " +str(post.get('address')) + " " + "Monthly Bill is" + "  " + vari

        }

        lead = request.env['crm.lead'].create(lead)
        print(request.session['bill'])
        # request.env['crm.lead'].create(lead)

        return request.redirect('/calendar/schedule-a-demo-5')




class billform(http.Controller):

    @http.route('/bill', auth='public', website='True', csrf=False)
    def index(self, **post):
        print(post.get('bill'))
        request.session['bill'] = int(post.get('bill'))
        print("in index action view")
        return request.render('ol_website.visitorform')

        # if post.get("bill") == None:
        #     return request.redirect('/calendar/schedule-a-demo-1')
        # else:
        #     return request.render('ol_website.bill')


class tips(http.Controller):

    # @http.route('/tips', auth='public', website='True')
    @http.route(['/tips'], type='http', auth="public", website=True, csrf=False)
    def index(self, **post):
        print(post.get('option'))
        if post.get("option") != 'ownhouse':
            print(post.get('option'))
            return request.render('ol_website.tips')
        else:
            return request.render('ol_website.bill')

class inheritincompany(models.Model):
    _inherit = 'project.project'

    another_date = fields.Datetime(default=fields.Datetime.now())
    project_expiry=fields.Datetime()

    @api.constrains('partner_id')
    def get_customer_id(self):
        partner = self.partner_id
        print(partner.name)
        context = ['Sunrun','Maximo Solar Industries','Planet Solar and Power']
        if partner.name not in context:
            company = self.env.user.company_id
            print(company)
            for rec in self:
                if rec.another_date:
                    project_expiry = rec.another_date + relativedelta(days=company.expiry_days)
                    rec.project_expiry = project_expiry
        else:
            print('hope')




class inheritincompanyfield(models.Model):
    _inherit = 'res.company'

    expiry_days=fields.Integer(string='Project Expiry Days')


    def company_id(self):
        active_id = self.env.user.company_id
        print(active_id)



# class inheritincompany(models.Model):
#     _inherit = 'crm.lead'
#
#     lead = {
#         'name': str(partner.name) + ':-' + str(rec.contact_no), 'user_id': False, 'team_id': False,
#         'partner_id': partner.id, 'phone': rec.contact_no, 'email_from': rec.email,
#
#     }
#     self.env['crm.lead'].create(lead)

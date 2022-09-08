# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2021. All rights reserved.

{
    'name': 'Odoo Twilio SMS Integration',
    'version': '15.0.0.0',
    'category': 'Tools',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Twilio - Odoo Integration',
    'website': 'http://www.technaureus.com/',
    'price': 49.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'description': """ 
    Integrating Twilio with Odoo.
""",
    'depends': ['contacts', 'website_sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/twilio_sms_views.xml',
        'views/res_config_views.xml',
        'views/res_partner_views.xml',
        'views/contact_list_views.xml',
        'wizard/twilio_wizard_views.xml',
        'wizard/message_wizard_views.xml',
    ],
    'demo': [
    ],
    'images': ['images/main_screenshot.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}

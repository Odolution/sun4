# Copyright 2019-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).

{
    'name': "Sale Payment Method ",
    'summary': """Adds the payment method on the Customer and the Sale Order. """,
    'version': "15.0.1.0.0",
    'category': 'Sale',
    'website': "http://sodexis.com/",
    'author': "Sodexis",
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'depends': [
        'account',
        'sale',
    ],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_view.xml',
        'views/invoice_view.xml'
    ],
    'images': ['images/main_screenshot.png'],
}

# -*- coding: utf-8 -*-


{
    'name': 'OL Project SMS Extension',

    "author": "Usama Shahid",
    'version': '0.1',
    'category': 'Project',
    'sequence': 95,
    'summary': 'Custom Requirements of sun4 for twilio SMS and Project.',
    'description': "Custom Requirements of sun4 for twilio SMS and Project.",
    'website': '',
    'images': [
    ],
    'depends': [
        'tis_twilio_integration','project'
        
    ],
    'data': [
        
        "views/project_ext.xml",
        "views/twilio.xml"
        
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
    ],
    'license': 'LGPL-3',
}

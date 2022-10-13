# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# YTI FIXME: This module should be named timesheet_enterprise
{
    'name': "Timesheets Grid Location",
    'summary': "Timesheets Grid Location View Inherit",
    'description': """
    Timesheets Grid Location View Inherit
    """,
    'version': '1.0',
    'depends': ['timesheet_grid'],
    'category': 'Services/Timesheets',
    'sequence': 65,
    'data': [
        'views/account_analytic_line.xml',
    ],
    'demo': [
    ],
    'application': True,
    'license': 'OEEL-1',
    'assets': {
        'web.assets_backend': [
            'timesheet_grid_location/static/src/js/timesheet_grid_renderer.js',
        ],
    }
}

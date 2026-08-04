# -*- coding: utf-8 -*-
{
    'name': 'OBIDSS Operational BI',
    'version': '18.0.1.0.0',
    'category': 'Business Intelligence',
    'summary': 'Custom Operational BI Dashboard and Reporting for PT Prima Alat Nusantara',
    'description': """
        OBIDSS Custom Odoo Operational BI Addon
        =======================================
        Integrates PT Prima Alat Nusantara (Company ID: 2, FY 2026) operational dashboards
        into Odoo 18 Dashboards application.
    """,
    'author': 'Senior Odoo BI Engineer',
    'website': 'https://github.com/Arilano14',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'sale_management',
        'purchase',
        'stock',
        'account',
        'spreadsheet_dashboard',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/dashboard_groups.xml',
        'views/obidss_data_quality_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

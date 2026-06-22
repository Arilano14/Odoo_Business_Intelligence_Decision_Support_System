{
    'name': 'Enterprise Business Intelligence',
    'version': '18.0.1.0.0',
    'category': 'Hidden/Tools',
    'summary': 'Native BI Tools for Sales and Purchase Analytics',
    'description': """
        Business Intelligence module directly integrated into Odoo.
        Provides a unified dashboard for Sales and Purchase data using native Odoo Views.
    """,
    'author': 'Arice Project',
    'depends': ['sale_management', 'purchase', 'board'],
    'data': [
        'views/analytics_actions.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

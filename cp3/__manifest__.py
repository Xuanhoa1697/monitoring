{
    "name": "Monitoring Realtime",
    "summary": """
    - Monitoring Realtime
""",
    "description": """
    Monitoring Realtime
""",
    "category": "Extra Tools",
    "author": "API",
    "version": "1.0.0",
    "depends": ['base','mail','report_xlsx'],
    'data': [
        'data/export_data.xml',
        'security/monitoring_security.xml',
        'security/ir.model.access.csv',
        'views/construction_monitoring_views.xml',
        'views/monitoring_sites_views.xml',
        'views/construction_monitoring_devices_views.xml',
        'views/monitoring_data_views.xml',
        'views/inclinometer_file_views.xml',
        'views/monitoring_compute_views.xml',
        'wizards/monitoring_data_wizard.xml',
        'views/menu_items.xml',
        'views/templates.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    "installable": True,
    "auto_install": False,
}

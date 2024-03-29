# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Base report xlsx",
    "summary": "Base module to create xlsx report",
    "author": "ACSONE SA/NV," "Creu Blanca," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/reporting-engine",
    "category": "Reporting",
    "version": "14.0.1.0.6",
    "development_status": "Production/Stable",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": ["xlsxwriter", "xlrd", "openpyxl"]},
    "depends": ["base", "web", "mail"],
    "data": [
        "data/ir_actions_report_data.xml",
        "views/webclient_templates.xml",
    ],
    'qweb': [
        'static/src/xml/report.xml',
    ],
    "installable": True,
    }

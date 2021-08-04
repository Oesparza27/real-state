# Copyright 2021, OmarEsparza
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Estate',
    'summary': 'Module summary',
    'version': '13.0.1.0.0',
    'category': 'Real State',
    'website': 'https://www.jarsa.com.mx/',
    'author': 'OmarEsparza',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
    ],
}

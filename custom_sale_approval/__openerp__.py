# -*- coding: utf-8 -*-
{
    'name': "Sales Approval",
    'images': ['static/description/config.png'],
    'summary': """
        Add Multi-level Hierarchy for exceeding credit limit""",

    'description': """
        This module is used to add extra configuration features and extra level in the sales employees hierarchy.\n
	
	-Agent \n
	-Officer \n
	-Manager \n

	In the configuration exceeding the credit limit for each type can be defined as follows:
	
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

  
    'category': 'Sales',
    'version': '1.0',

    'depends': ['base', 'sale_crm', 'stock', 'sale', 'purchase'],

    'data': [
        'views.xml',
'security/security.xml',
'templates.xml',
    ],
}

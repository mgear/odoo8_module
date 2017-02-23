# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'System Filters Security',
    'version': '0.1',
    'category': 'Access Rights',
    'author': 'Tamkeen Technologies',
    'website': 'http://tamkeentech.sa/',
    'description': """
Filters Security:
#####################################
- Prevent the normal users from removing the filters where it can be used as filter fro the system templates not only for searching.
""",
    'depends': [
        'base', 
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

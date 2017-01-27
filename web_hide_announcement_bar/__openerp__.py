{
    'name': 'Hide Announcement Bar',
    'version': '0.1',
    'category': 'Tools',
    'depends': ['mail'],
    'author': "JRELA Soft",
    'website': "www.linkedin.com/in/jrelasoft",
    'description': """
        Module which hides the Odoo announcement bar.
    """,
    'data': ['templates.xml'],
    'images': [],
    'js': ['static/src/js/announcement.js'],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'installable': True,
    'active': False,
}

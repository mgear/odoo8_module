# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Today Synconics Technologies Pvt. Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

{
    "name": "Drag & Drop Multi Attachments", 
    "version": "1.0", 
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'https://www.synconics.com',
    "category": "Social Network",
    "summary": "Drag & Drop multiple attachments in the form view at once",
    "description": """
    This module enables the feature to Drag & Drop multiple attachments in the form view of any objects.
 
    The attachments which are selected can simply drag &amp; drop to the form view and will be available at the "Attachments" dropdown box on the top of the form view.
 
    To attach the files in the Odoo object, You have to open the form view, explore the file(s), select the file(s) and drag & drop them into the “Drop your files here” area of the form view.
    
    Dropped files will be available in the “Attachments” dropdown box on the top of the form view.
    
    Installation Requirements:
    ==========================
    
    To install this module, make sure you have installed "sync_mail_multi_attach" dependency module.
    
    Download Link: https://www.odoo.com/apps/modules/8.0/sync_mail_multi_attach/
    
    Video Demo Link:
    ================
    
    https://www.youtube.com/watch?v=v1CD1owx8_8
    """,
    "depends": ["document", "sync_mail_multi_attach"],
    'data': ["views/drag_drop_attach_view.xml"],
    'qweb': ['static/src/xml/*.xml'],
    "price": 35,
    "currency": "EUR", 
    "installable": True, 
    "auto_install": False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

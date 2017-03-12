# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 OpenERP s.a. (<http://openerp.com>).
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
	'name': 'leads with product in crm',
	'version': '1.0',
	'author': 'Brijesh Kesariya / Merlin TecSol Pvt. Ltd.',
	'category': 'CRM',
	'website': 'http://www.merlintecsol.com',
	'license': 'GPL-3',
	'data': [],
	'update_xml': ["custom_crm_view.xml"],
	'depends': ['crm','sale_crm','sale'],
	'installable': True,
	'active': True,
	'auto_install': False,
	'Description': "This is a small module which adds the Product in it.You can view and group by your Inquiries Productwise.More than that, while creating the Quatation directly from lead or opportunity the Product in Quatation added automatically from the Lead.",

}

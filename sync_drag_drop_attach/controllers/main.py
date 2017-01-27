# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#    Copyright (C) 2011-today Synconics Technologies Pvt. Ltd. (<http://www.synconics.com>)
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
import os
import zipfile
import StringIO
import functools
import base64
import mimetypes
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import content_disposition
from openerp.addons.web.controllers.main import _serialize_exception
import werkzeug
from openerp.addons import mail
from openerp.addons import web
import logging

try:
    import simplejson as simplejson
except ImportError:
    import json     # noqa
    
def serialize_exception(f):
    _logger = logging.getLogger(__name__)

    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(simplejson.dumps(error))
    return wrap

class Binary(web.controllers.main.Binary):

    @http.route('/web/binary/upload_attachment', type='http', auth="user", csrf=False)
    @serialize_exception
    def upload_attachment(self, callback, model, id, ufile, multi=False):
        if multi:
            Model = request.session.model('ir.attachment')
            out = """<script language="javascript" type="text/javascript">
                    var win = window.top.window;
                    win.jQuery(win).trigger(%s, %s);
                </script>"""
            try:
                attachment_id = Model.create({
                    'name': ufile.filename,
                    'datas': base64.encodestring(ufile.read()),
                    'datas_fname': ufile.filename,
                    'res_model': model,
                    'res_id': int(id)
                }, request.context)
                args = {
                'filename': ufile.filename,
                'id':  attachment_id
                }
            except Exception:
                args = {'error': "Something horrible happened"}
                return out % (simplejson.dumps(callback), simplejson.dumps(args))
            return str(attachment_id)
        else:
            return super(Binary, self).upload_attachment(callback, model, id, ufile)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

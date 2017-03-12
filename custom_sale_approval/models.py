from openerp import SUPERUSER_ID
from openerp import models, fields, api, _
from openerp.osv import osv
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model): ## A new Class to modify the sales
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.v7
    def action_button_request_for_approval(self, cr, uid, ids, context=None): # A button to request approval
        effective_credit_limit, partner_id = self._get_effective_credit_limit(cr, ids, uid, context=context)
        so_obj = self.browse(cr, uid, ids, context=context)
        manager_value=self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'managerrequired')
        SeniorLimit = self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'senior_limit')
        ManagerLimit = self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'manager_limit')
        officer_value=self.pool.get("ir.config_parameter").get_param(cr, uid, 'officerrequired_value')
        final_manager_value=bool(manager_value)
        final_officer_value=bool(officer_value)
        flag_manager = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_manager') 
        flag_officer = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_officer') 
        flag_agent = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_agent') 
        num = so_obj.amount_total - (partner_id.credit_limit - effective_credit_limit)
        den = (partner_id.credit_limit - effective_credit_limit)
            
        if (flag_officer is True):
            return self.write(cr, uid, ids[0], {'state': 'manager_approval'}, context=context)
        elif(flag_agent is True):
            if (so_obj.amount_total <= partner_id.credit_limit - effective_credit_limit):
                if((final_officer_value is True) or (final_officer_value is False and final_manager_value is False)):
                    return self.write(cr, uid, ids[0], {'state': 'officer_approval'}, context=context)
                else:
                    return self.write(cr, uid, ids[0], {'state': 'manager_approval'}, context=context)
            else:
                if  (num/den)*100 <= SeniorLimit :
                    return self.write(cr, uid, ids[0], {'state': 'officer_approval'}, context=context)
                
                elif (num/den)*100 <= ManagerLimit :
                    return self.write(cr, uid, ids[0], {'state': 'manager_approval'}, context=context)   
                else:
                    raise osv.except_osv(_('Error!'), _("Sales order can't be created becuase this customer exceeded the credit limit"))
            
        else:
            raise osv.except_osv(_('Error!'), _("You don't have the required authority for this action, Please contact the administrator"))
            
    @api.v7
    def action_button_reject(self, cr, uid, ids, context=None):
        so_obj = self.browse(cr, uid, ids[0], context=context)  # Reject the request but must write the reason for rejection
        if not so_obj.note:
            raise osv.except_osv(_('Error!'), _('You have to write down a note (Reject Reason).'))
        else:
            return self.write(cr, uid, ids[0], {'state': 'rejected'}, context=context)

  
    @api.v7
    def action_button_confirm(self, cr, uid, ids, context=None): #check before approval if the credit limit will be exceeded or not
        effective_credit_limit, partner_id = self._get_effective_credit_limit(cr, ids, uid, context=context)
        so_obj = self.browse(cr, uid, ids, context=context)
        manager_value=self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'managerrequired')
        officer_value=self.pool.get("ir.config_parameter").get_param(cr, uid, 'officerrequired_value')
        final_manager_value=bool(manager_value)
        final_officer_value=bool(officer_value)
        flag_manager = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_manager') 
        flag_officer = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_officer') 
        flag_agent = self.pool.get('res.users').has_group(cr, uid, 'sales_auto_crm.group_sale_approval_agent') 
        num = so_obj.amount_total - (partner_id.credit_limit - effective_credit_limit)
        den = (partner_id.credit_limit - effective_credit_limit)
        SeniorLimit = self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'senior_limit')
        ManagerLimit = self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'manager_limit') 
        #groups_id = self.pool.get('res.users').read(cr, uid, uid)['groups_id']
        #_logger.error("current user group : %r", flag)

        if(flag_manager is True):
            return super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
        elif (flag_officer is True and so_obj.state != 'manager_approval'):
            if (so_obj.amount_total <= partner_id.credit_limit - effective_credit_limit) or (num/den)*100 < SeniorLimit:
                if(final_manager_value is False ):
                    return super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
                else:
                    raise osv.except_osv(_('Error!'), _("You have to request for approval first, As you don't have the authority"))
            else:
                raise osv.except_osv(_('Error!'), _("You have to request for approval first, As you the current customer exceeds the credit limit"))
        elif (flag_agent is True):
            if (so_obj.amount_total <= partner_id.credit_limit - effective_credit_limit):
                if(final_manager_value is False and final_officer_value is False):
                    return super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
                else:
                    raise osv.except_osv(_('Error!'), _("You have to request for approval first, As you don't have the required authority")) 
            else:
                raise osv.except_osv(_('Error!'), _("You have to request for approval first, As you the current customer exceeds the credit limit"))
        else:
            raise osv.except_osv(_('Error!'), _("You don't have the required authority, Please contact the administrator"))
        

       
    @api.v7
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None): #when saving sales order the amount of order will be checked if it exceeds the limit and its state is draft and requiest manger approval else reject the sales order
        effective_credit_limit, partner_id = self._get_effective_credit_limit(cr, ids, uid, context=context)
        so_obj = self.browse(cr, uid, ids[0], context=context)
        res = super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context=context) # return tha total amount of invoice
        
        manager_value=self.pool.get('ir.values').get_default(cr,uid,'sale.config.settings', 'managerrequired')
        officer_value=self.pool.get("ir.config_parameter").get_param(cr, uid, 'officerrequired_value')
        final_manager_value=bool(manager_value)
        final_officer_value=bool(officer_value)
        for key in res:
                num = res[key]['amount_total'] - (partner_id.credit_limit - effective_credit_limit)
                den = (partner_id.credit_limit - effective_credit_limit)
                if res[key]['amount_total'] > partner_id.credit_limit - effective_credit_limit:
                    if so_obj.request_for_manager_approval is True:
                        raise osv.except_osv(_('Error!'), _(
                            'You can not create the sales order with the current amount as it exceeds the credit limit allowed to this customer. Please check Require Manager Approval box'))
        return res 
        

    def _get_effective_credit_limit(self, cr, ids, uid, context=None): # return the credit limit of this customer
        sale_order_obj = self.browse(cr, uid, ids, context=context)
        partner_id = sale_order_obj[0].partner_id
        invoice_pool = self.pool.get('account.invoice')
        
        confirmed_so_ids = self.search(cr, uid,
                                       [('state', 'in', ['progress', 'manual', 'officer_approval', 'manager_approval']), ('partner_id', '=', partner_id.id),
                                        ('invoice_exists', '=', False)], context=context)
        confirmed_so_objs = self.browse(cr, uid, confirmed_so_ids, context=context)
        total_confirmed_so = sum([so.amount_total for so in confirmed_so_objs])
        ### Draft Invoices
        draft_invoice_ids = invoice_pool.search(cr, uid,
                                                [('state', 'in', ['draft']), ('partner_id', '=', partner_id.id)])
        draft_invoice_objs = invoice_pool.browse(cr, uid, draft_invoice_ids, context=context)
        total_draft_invoices = sum([draft_invoice.amount_total for draft_invoice in draft_invoice_objs])
        ### Confirmed Invoices that have balance
        confirmed_invoice_ids = invoice_pool.search(cr, uid,
                                                    [('state', 'in', ['open']), ('partner_id', '=', partner_id.id),
                                                     ('residual', '!=', False)])
        confirmed_invoice_objs = invoice_pool.browse(cr, uid, confirmed_invoice_ids, context=context)
        total_confirmed_invoices = sum([confirmed_invoice.residual for confirmed_invoice in confirmed_invoice_objs])
        effective_credit_limit = total_confirmed_invoices + total_confirmed_so + total_draft_invoices
        return effective_credit_limit, partner_id

    @api.constrains('partner_id') ##check if this customer is blocked or not
    def _check_blocked_user(self):
        if self.partner_id.block:
            raise osv.except_osv(_('Error!'),
                                 _('This customer is blocked, you will not be able to create SO for this Customer.'))

    @api.one
    @api.depends('partner_id', 'amount_total')
    def _get_allowed_credit(self):
        invoice_pool = self.env['account.invoice']
        confirmed_so_objs = self.search([('state', 'in', ['progress', 'manual', 'officer_approval', 'manager_approval']), ('partner_id', '=', self.partner_id.id),
                                        ('invoice_exists', '=', False)])
        total_confirmed_so = sum([so.amount_total for so in confirmed_so_objs])
        ### Draft Invoices
        draft_invoice_objs = invoice_pool.search([('state', 'in', ['draft']), ('partner_id', '=', self.partner_id.id)])
        total_draft_invoices = sum([draft_invoice.amount_total for draft_invoice in draft_invoice_objs])
        ### Confirmed Invoices that have balance
        confirmed_invoice_objs = invoice_pool.search([('state', 'in', ['open']), ('partner_id', '=', self.partner_id.id),
                                                     ('residual', '!=', False)])
        total_confirmed_invoices = sum([confirmed_invoice.residual for confirmed_invoice in confirmed_invoice_objs])
        effective_credit_limit = total_confirmed_invoices + total_confirmed_so + total_draft_invoices
        self.allowed_credit = self.partner_id.credit_limit - effective_credit_limit

    request_for_manager_approval = fields.Boolean(string="Request Credit Limit Exception", )
    allowed_credit = fields.Float(string="Allowed Credit", compute="_get_allowed_credit", )

    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('cancel', 'Cancelled'),
        ('waiting_date', 'Waiting Schedule'),
        ('progress', 'Sales Order'), ('manager_approval', 'Manager Approval'),
        ('manual', 'Sale to Invoice'), ('officer_approval', 'Senior Approval'),
        ('shipping_except', 'Shipping Exception'),
        ('invoice_except', 'Invoice Exception'), ('rejected', 'Rejected'),
        ('done', 'Done'),
    ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True)

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    block = fields.Boolean(string="Block", )
    
    @api.v7
    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False,
                   lazy=True):
        ret_val = super(res_partner, self).read_group(cr, uid, domain, fields, groupby, offset=offset, limit=limit,
                                                      context=context, orderby=orderby, lazy=lazy)
        for rt in ret_val:
            if rt.has_key('block'):
                if rt.get('block', False):
                    rt['block'] = 'Blocked Customers'
                else:
                    rt['block'] = 'Allowed Customer'
        return ret_val



class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)

        # the method will check if the amount_total exceeds the credit_limit or not!
        self.amount_total = self.amount_untaxed + self.amount_tax

        sale_order_objs = self.env['sale.order'].search(
                [('partner_id', '=', self.partner_id.id), ('state', 'in', ['progress', 'manual']),
                 ('invoice_exists', '=', False)])

        total_confirmed_so = sum([so.amount_total for so in sale_order_objs])
        ### Draft Invoices
        draft_invoice_objs = self.search(
                [('state', 'in', ['draft']), ('partner_id', '=', self.partner_id.id), ('id', 'not in', self.ids)])
        total_draft_invoices = 0
        total_draft_invoices = sum([draft_invoice.amount_total for draft_invoice in draft_invoice_objs])
        ### Confirmed Invoices that have balance
        confirmed_invoice_objs = self.search([('state', 'in', ['open']), ('partner_id', '=', self.partner_id.id),
                                              ('residual', '!=', False)])
        total_confirmed_invoices = 0
        total_confirmed_invoices = sum([confirmed_invoice.residual for confirmed_invoice in confirmed_invoice_objs])
        effective_credit_limit = total_confirmed_invoices + total_confirmed_so + total_draft_invoices

        if self.amount_total > self.partner_id.credit_limit - effective_credit_limit:
            raise osv.except_osv(_('Error!'), _(
                    'You can not create the invoice with the current amount as it exceeds the credit limit allowed to this customer.'))


class auto_sales_Settings(models.TransientModel):
    _inherit = 'sale.config.settings'
    _name = 'sale.config.settings'
    

    
    senior_limit = fields.Integer(string="%     Senior Credit limit exception Percentage",help="The allowed percentage for senior to approve" )
    manager_limit = fields.Integer(string="%    Manager Credit limit exception Percentage",help="The allowed percentage for manager to approve")
    managerrequired = fields.Boolean(string="Require Manager Approval",help="Check this box to require manager approval in all sale orders")
    officerrequired = fields.Boolean(string="Require Senior Approval",help="Check this box to require senior approval in all sale orders")
    # GETS: latest data    
    def get_default_officerrequired(self, cr, uid, ids, context=None):  
        param_obj = self.pool.get("ir.config_parameter")      
        res = {'officerrequired': param_obj.get_param(cr, uid, 'officerrequired_value')}        
        return res
    
    # POST: saves new data    
    def set_values(self, cr, uid, ids, context=None):
        param_obj = self.pool.get("ir.config_parameter")
        param_val = self.browse(cr, uid, ids, context=context).officerrequired
        for record in self.browse(cr, uid, ids, context=context):
            param_obj.set_param(cr, uid, 'officerrequired_value',param_val or "")

    def set_managerrequired_defaults(self, cr, uid, ids, context=None):
        sale_price = self.browse(cr, uid, ids, context=context).managerrequired
        res = self.pool.get('ir.values').set_default(cr, uid, 'sale.config.settings', 'managerrequired', sale_price)
        return res

    def set_senior_limit_defaults(self, cr, uid, ids, context=None):
        sale_price = self.browse(cr, uid, ids, context=context).senior_limit
        if(self.browse(cr, uid, ids, context=context). manager_limit < self.browse(cr, uid, ids, context=context). senior_limit):
            raise osv.except_osv(_('Error!'), _('Manager Limit must be greater than or equal the officer limit.'))
        res = self.pool.get('ir.values').set_default(cr, uid, 'sale.config.settings', 'senior_limit', sale_price)
        return res

    def set_manager_limit_defaults(self, cr, uid, ids, context=None):
        sale_price = self.browse(cr, uid, ids, context=context). manager_limit
        if(self.browse(cr, uid, ids, context=context). manager_limit < self.browse(cr, uid, ids, context=context). senior_limit):
            raise osv.except_osv(_('Error!'), _('Manager Limit must be greater than or equal the officer limit.'))
        res = self.pool.get('ir.values').set_default(cr, uid, 'sale.config.settings', 'manager_limit', sale_price)
        return res


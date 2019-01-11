# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from odoo import api, fields, models, _



class SaleQuotes(models.Model):
    _name = "sale.quotes"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Sales Quotes"
    _order = 'date_order desc, id desc'

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


    @api.model
    def _default_note(self):
        return self.env.user.company_id.sale_note

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed on the SO.
        """
        for order in self:
            order.order_line._compute_tax_id()

    def _inverse_project_id(self):
        self.project_id = self.related_project_id

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    origin = fields.Char(string='Source Document', help="Reference of the document that generated this sales order request.")
    client_order_ref = fields.Char(string='Customer Reference', copy=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('sale', 'Sale'),
        ('done', 'Confirm'),
        ('cancel', 'Cancel'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    date_order = fields.Datetime(string='Quotes Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    validity_date = fields.Date(string='Expiration Date', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")
    create_date = fields.Datetime(string='Creation Date', readonly=True, index=True, help="Date on which sales quote is created.")
    confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current sales order.")
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.")

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Pricelist for current sales order.")
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    project_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order.", copy=False)
    related_project_id = fields.Many2one('account.analytic.account', inverse='_inverse_project_id', related='project_id', string='Analytic Account', help="The analytic account related to a sales order.")

    order_line = fields.One2many('sale.quote.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    note = fields.Text('Terms and conditions', default=_default_note)

    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')

    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position', string='Fiscal Position')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    team_id = fields.Many2one('crm.team', 'Sales Team', change_default=True, default=_get_default_team, oldname='section_id')
    procurement_group_id = fields.Many2one('procurement.group', 'Procurement Group', copy=False)

    product_id = fields.Many2one('product.product', related='order_line.product_id', string='Product')

    # 所有通关信息
    import_and_export = fields.Selection(
        [('i', 'Import'), ('e', 'Export'), ('n', 'None')],
        'Type of Import and Export',
        required=True,
        default='n'
    )
    transport = fields.Many2one('delegate_transport_mode', 'Transport Mode', required=True)
    exemption = fields.Many2one('delegate_exemption', 'Cut Mode')
    trade_term = fields.Many2one('delegate_trade_terms', string='Transaction Mode')
    port = fields.Many2one('delegate_port', string='Port')
    num = fields.Integer('Number')
    gross_weight = fields.Float('Gross Weight')
    mark_code = fields.Char('Mark Code')
    remarks = fields.Text('Remarks')

    customs = fields.Many2one('delegate_customs', string='Customs')
    trade_mode = fields.Many2one('delegate_trade_mode', string='Trade Mode')
    trade_country = fields.Many2one('delegate_country', string='Trade Country')
    origin_arrival_country = fields.Many2one('delegate_country', string='Origin And Arrival Country')
    region = fields.Many2one('delegate_region', string='Region')
    packing = fields.Many2one('delegate_packing', string='Wrap Mode')
    net_weight = fields.Float('Net Weight')
    # delegate_id = fields.Many2one('delegation_list', string='委托清单名')  # 询价单是否关联委托清单

    multi_currency = fields.Selection([('True', 'Multi Currency'), ('False', 'Single currency')],
                                      'Currency', default='False')

    @api.model
    def _get_customer_lead(self, product_tmpl_id):
        return False

    @api.multi
    def button_dummy(self):
        return True

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'sale':
            return 'sale.mt_order_confirmed'
        elif 'state' in init_values and self.state == 'sent':
            return 'sale.mt_order_sent'
        return super(SaleQuotes, self)._track_subtype(init_values)

    @api.multi
    @api.onchange('partner_shipping_id', 'partner_id')
    def onchange_partner_shipping_id(self):
        """
        Trigger the change of fiscal position when the shipping address is modified.
        """
        self.fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id, self.partner_shipping_id.id)
        return {}

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment term
        - Invoice address
        - Delivery address
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        if self.env.user.company_id.sale_note:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note

        if self.partner_id.user_id:
            values['user_id'] = self.partner_id.user_id.id
        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        warning = {}
        title = False
        message = False
        partner = self.partner_id

        # If partner has no warning, check its company
        if partner.sale_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id

        if partner.sale_warn != 'no-message':
            # Block if partner only has warning but parent company is blocked
            if partner.sale_warn != 'block' and partner.parent_id and partner.parent_id.sale_warn == 'block':
                partner = partner.parent_id
            title = ("Warning for %s") % partner.name
            message = partner.sale_warn_msg
            warning = {
                    'title': title,
                    'message': message,
            }
            if partner.sale_warn == 'block':
                self.update({'partner_id': False, 'partner_invoice_id': False, 'partner_shipping_id': False, 'pricelist_id': False})
                return {'warning': warning}

        if warning:
            return {'warning': warning}

    @api.model
    def create(self, vals):
        """
        重新设计订单号的生成，加入进出口类型，运输方式，日期等参数
        :param vals:
        :return:
        """
        if vals.get('name', _('New')) == _('New'):
            transport = self.env['delegate_transport_mode'].browse(vals['transport'])
            import_and_export = vals['import_and_export'].upper()

            tran_dic = {
                '5': 'AIR',
                '2': 'SEA',
                '6': 'POST',
                '4': 'LAND',
            }

            tran_code = tran_dic[transport.Code] if transport.Code in tran_dic else  ''

            # import pytz
            # tz = pytz.timezone('Asia/Shanghai')
            local_time = fields.datetime.now().strftime('%y%m')
            name = 'BYJC' + tran_code + import_and_export + local_time
            qsets = self.search([('name', 'like', '%'+local_time+'%')])
            print(qsets)
            if len(qsets) == 0:
                num = 1
            else:
                name_sets = []
                for i in qsets:
                    s = i.name[-3:]
                    name_sets.append(int(s))
                num = max(name_sets) + 1
            vals['name'] = (name + '%03d')%num
            print(vals['name'])

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        print(vals)
        result = super(SaleQuotes, self).create(vals)
        return result


    @api.multi
    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'sale.report_saleorder')

    @api.multi
    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancel', 'sent'])
        orders.write({
            'state': 'draft',
            'procurement_group_id': False,
        })
        orders.mapped('order_line').mapped('procurement_ids').write({'sale_line_id': False})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_quotation_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('sales+custom', 'email_template_edi_sale')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict()
        ctx.update({
            'default_model': 'sale.quotes',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "sale.mail_template_data_notification_email_sale_order"
        })
        print(ctx)
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def force_quotation_send(self):
        for order in self:
            email_act = order.action_quotation_send()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=order.company_id.email)
                order.with_context(email_ctx).message_post_with_template(email_ctx.get('default_template_id'))
        return True

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    def _prepare_procurement_group(self):
        return {'name': self.name}

    @api.multi
    def action_confirm(self):
        for order in self:
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()
        return True

    @api.multi
    def _create_analytic_account(self, prefix=None):
        for order in self:
            name = order.name
            if prefix:
                name = prefix + ": " + order.name
            analytic = self.env['account.analytic.account'].create({
                'name': name,
                'code': order.client_order_ref,
                'company_id': order.company_id.id,
                'partner_id': order.partner_id.id
            })
            order.project_id = analytic

    @api.multi
    def order_lines_layouted(self):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(self.order_line, lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })

        return report_pages

    @api.multi
    def _get_tax_amount_by_group(self):
        self.ensure_one()
        res = {}
        currency = self.currency_id or self.company_id.currency_id
        for line in self.order_line:
            base_tax = 0
            for tax in line.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, 0.0)
                amount = tax.compute_all(line.price_reduce + base_tax, quantity=line.product_uom_qty,
                                         product=line.product_id, partner=self.partner_shipping_id)['taxes'][0]['amount']
                res[group] += amount
                if tax.include_base_amount:
                    base_tax += tax.compute_all(line.price_reduce + base_tax, quantity=1, product=line.product_id,
                                                partner=self.partner_shipping_id)['taxes'][0]['amount']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = map(lambda l: (l[0].name, l[1]), res)
        return res


class SaleQuoteLine(models.Model):
    _description = '报价单对应的产品订单行，也需要单独建表。除关联的订单外，结构一样'
    _name = 'sale.quote.line'
    _inherit = 'sale.order.line'

    # order_id = fields.Many2one('sale.quotes', string='Quote Reference', ondelete='cascade', index=True, copy=False)


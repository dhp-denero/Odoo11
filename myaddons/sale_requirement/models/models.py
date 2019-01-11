# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
import datetime
from datetime import datetime


class StockAppendPurchasePlan(models.TransientModel):
    _name = 'quotation.cycle.append'

    plan_id = fields.Many2one('quotation.cycle', string='Purchase Plan')
    partner_id = fields.Many2one('res.partner', string='Submitter', default=lambda self: self.env.user.partner_id)
    request = fields.Text(string='Description')
    requirement_id = fields.Many2one('sale.requirement', string='Requirement', related='plan_id.requirement_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    name = fields.Char(string='Plan Name')
    description = fields.Text(string='Description')

    # 供应链用

    def create_purchase_plan(self):
        notes = self.env['product.quotation'].browse(self.env.context.get('active_ids'))
        vals = {'partner_id': self.partner_id.id,
                'name': self.name,
                'requirement_id': notes[0].requirement_id.id,
                'description': self.request,
                'currency_id': self.currency_id.id,
                }
        order_id = self.env['quotation.cycle'].create(vals)
        for product in notes:
            order_id.write({
                'cycle_line': [
                    (0, 0, {
                        'product_id': product.product_chose.product_id.id,
                        'quote_id': product.id,
                        'name': product.customer_description,
                        'partner_id': self.partner_id.id,
                    })]
            })
            view_id = self.env.ref('sale_requirement.view_purchase_plan_form')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'quotation.cycle',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_id': order_id.id,
                'view_id': view_id.id,
            }

    def add_to_purchase_plan(self):
        notes = self.env['product.quotation'].browse(self.env.context.get('active_ids'))
        for product in notes:
            self.plan_id.write({
                'cycle_line': [
                    (0, 0, {
                        'product_id': product.product_chose.product_id.id,
                        'quote_id': product.id,
                        'name': product.customer_description,
                        'partner_id': self.partner_id.id,
                    })]
            })
            view_id = self.env.ref('sale_requirement.view_purchase_plan_form')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'quotation.cycle',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_id': self.plan_id.id,
                'view_id': view_id.id,
            }


class CyclePurchaseOrder(models.Model):
    _name = 'quotation.cycle'

    name = fields.Char(string='Plan Name')
    project_ref = fields.Char(string='Plan Code',
                              default=lambda self: self.env['ir.sequence'].next_by_code('cycle.project'))
    requirement_id = fields.Many2one('sale.requirement', string='Requirement')
    company_id = fields.Many2one('res.partner', related='partner_id.parent_id', string='Company')
    partner_id = fields.Many2one('res.partner', string='Submitter')
    state = fields.Selection(
        [('red', 'Pending'),
         ('green', 'Approved'),
         ('black', 'Done')],
        string='state',
        default='red')
    product_count = fields.Integer(string='Product', compute='_number_of_cycle_product')
    date = fields.Date(string='Create Date', default=fields.Date.today())
    cycle_line = fields.One2many('quotation.cycle.line', 'order_id')
    description = fields.Text(string='Plan Description')
    total_price = fields.Float(string='Total Price', compute='compute_subtotal')
    delivery_time = fields.Datetime(string='Delivery Date')
    manager_id = fields.Many2one('res.partner', string='Plan Manager', ondelete='set null', index=True)
    product_needquote_count = fields.Integer(string='Need Quote', compute='_number_of_need_quote_product')
    currency_id = fields.Many2one('res.currency', string='Currency')
    color = fields.Integer(string='Color Index', default=10, compute="change_colore_on_kanban")

    @api.depends('state')
    @api.onchange('state')
    def change_colore_on_kanban(self):
        """    this method is used to chenge color index    base on fee status    ----------------------------------------    :return: index of color for kanban view    """
        for record in self:
            color = 0
            if record.state == 'black':
                color = 0
            elif record.state == 'green':
                color = 7
            elif record.state == 'red':
                color = 1
            record.color = color

    @api.depends()
    def _number_of_cycle_product(self):
        for s in self:
            domain = [('order_id', '=', s.id)]
            count = len(s.env['quotation.cycle.line'].search(domain).ids)
            s.product_count = count

    @api.depends()
    def _number_of_need_quote_product(self):
        for s in self:
            domain = [('price_rate', '=', False), ('order_id', '=', s.id)]
            count = len(s.env['quotation.cycle.line'].search(domain).ids)
            s.product_needquote_count = count

    # 计算需求预算
    @api.depends('cycle_line')
    def compute_subtotal(self):
        for product in self:
            product.total_price = 0
            for line in product.cycle_line:
                product.total_price += line.price_total_currency

    # 创建订单
    def action_create_order_new(self):
        vals = {'partner_id': self.partner_id.id,
                'user_id': self.partner_id.user_id.id,
                'requirement_id': self.requirement_id.id,
                'validity_date': self.delivery_time,
                'currency_id': self.currency_id.id,
                }
        sale_order = self.env['sale.order'].create(vals)
        order_line = self.env['sale.order.line']
        for line in self.cycle_line:
            pdt_value = {
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'name': line.description,
                'product_uom_qty': line.uom_qty,
                'uom_id': line.uom_id.id,
                'price_unit': line.market_price,
            }
            order_line.create(pdt_value)
        view_id = self.env.ref('sale.view_order_form')
        self.state = 'black'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': sale_order.id,
            'view_id': view_id.id,
        }


class CyclePurchaseOrder(models.Model):
    _name = 'quotation.cycle.line'

    name = fields.Char(string='Name', related='product_id.display_name')
    product_id = fields.Many2one('product.product', string='Product')
    categ_id = fields.Many2many('product.public.category', string='Category')
    uom_qty = fields.Float(string='Quantity')
    uom_id = fields.Many2one('product.uom', string='Unit')
    price_unit = fields.Float(string='COST', compute='_select_supplier')
    price_tax = fields.Float(string='TAX', compute='_compute_unit')
    no_duty_price = fields.Float(string='Price Excluded', compute='_compute_unit')
    market_price = fields.Float(string='Price', compute='_compute_unit')
    tax_total = fields.Float(string='Total Tax', compute='_compute_total')
    price_total = fields.Float(string='Total', compute='_compute_total')
    price_total_currency = fields.Float(string='Total', compute='_compute')
    market_price_currency = fields.Float(string='Unit Price', compute='_compute')
    quote_id = fields.Many2one('product.quotation', string='Quote')
    order_id = fields.Many2one('quotation.cycle', string='Order')
    description = fields.Text(string='Description')
    currency_id = fields.Many2one('res.currency', readonly=True, compute='_select_supplier')
    pricing_currency_id = fields.Many2one('res.currency')
    tax_id = fields.Many2many('account.tax', string='Taxes')
    partner_id = fields.Many2one('res.partner', string='Submitter')
    application = fields.Many2many('product.application', string='Application', related='quote_id.application')
    department = fields.Many2many('res.department', string='Department', related='quote_id.department')
    price_rate = fields.Float(string='费率')
    delay = fields.Float(string='Purchase Delay', compute='_select_supplier')
    complete_name = fields.Char(string='Name', compute='_compute_complete_name', store=True)

    _sql_constraints = [
        ('complete_name_uniq', 'unique (complete_name)', "Product already exists!"),
    ]

    @api.depends('product_id')
    def _compute_complete_name(self):
        for category in self:
            category.complete_name = '%s / %s / %s' % (
                category.quote_id.name, category.order_id.name, category.product_id.name)

    @api.onchange('partner_id', 'uom_qty', )
    @api.depends('partner_id', 'uom_qty')
    def _select_supplier(self):
        for line in self:
            for product in line.product_id:
                supplier = product._select_seller(quantity=line.uom_qty)
                line.price_unit = supplier.price
                line.currency_id = supplier.currency_id
                line.uom_id = supplier.product_uom
                line.delay = product.sale_delay

    # 通过汇率计算价格
    @api.depends('price_total', 'market_price', 'pricing_currency_id', 'currency_id', 'price_rate')
    def _compute(self):
        for order in self:
            if order.currency_id and order.pricing_currency_id and order.price_rate:
                order.price_total_currency = self.env['res.currency']._compute(order.currency_id,
                                                                               order.pricing_currency_id,
                                                                               order.price_total)
                order.market_price_currency = self.env['res.currency']._compute(order.currency_id,
                                                                                order.pricing_currency_id,
                                                                                order.market_price)

    # 计算毛利与成本
    @api.depends()
    def _compute_cost(self):
        for line in self:
            line.cost_total = line.price_unit * line.uom_qty
            line.margin = line.price_total - line.cost_total - line.tax_total

    # 计算人民币总价
    @api.depends('uom_qty', 'price_unit', 'tax_id', 'price_rate', 'product_id')
    def _compute_total(self):

        for line in self:
            if not line.price_rate:
                price = line.price_unit * (1 / (1 - line.product_id.compute_price_rate(product_id=line.product_id,
                                                                                       partner_id=line.order_id.company_id,
                                                                                       price_rate=line.price_rate)))
                taxes = line.tax_id.compute_all(price, line.currency_id, line.uom_qty, product=line.product_id,
                                                partner=line.order_id.company_id)
                line.update({
                    'tax_total': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                })

    # 计算单价，免税价
    @api.depends('price_unit', 'tax_id', 'price_rate', 'product_id')
    def _compute_unit(self):
        for line in self:
            price = line.price_unit * (1 / (1 - line.price_rate))
            taxes = line.tax_id.compute_all(price, line.currency_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'market_price': taxes['total_included'],
                'no_duty_price': taxes['total_excluded'],
            })


class ProductProductAppendSo(models.TransientModel):
    _name = 'product.product.append.br'

    quotation_id = fields.Many2one('product.quotation', string='Quotation')
    requirement_id = fields.Many2one('sale.requirement', related='quotation_id.requirement_id', string='Requirement')
    partner_id = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id)
    image = fields.Binary(related="product_id.image_medium")
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    name = fields.Char(string='Product Name')
    request = fields.Text(string='Customer Request')

    # 供应链用
    def apply_insert(self):
        self.quotation_id.write({
            'product_line': [
                (0, 0, {
                    'pdt_quote': self.quotation_id.id,
                    'pdt_requirement': self.requirement_id.id,
                    'product_id': self.product_id.id,
                    'name': self.request,
                    'partner_id': self.partner_id.id,
                })]
        })
        view_id = self.env.ref('sale_requirement.product_quotation_form')
        quotation_id = self.quotation_id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.quotation',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': quotation_id.id,
            'view_id': view_id.id,
        }


class Quotation_Product_Line(models.Model):
    _name = 'quotation.product.line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string="Product", copy=True,
                                 change_default=True, ondelete='cascade', required=True)
    pdt_requirement = fields.Many2one('sale.requirement', string='Requirement', ondelete="cascade",
                                      related='pdt_quote.requirement_id')
    name = fields.Text(string='Description')
    pdt_quote = fields.Many2one('product.quotation', string='Quote Product', ondelete="cascade", copy=True)
    application = fields.Many2many('product.application', string='Application', related='product_id.application')
    image = fields.Binary(string='Image', related='product_id.image_medium')
    categ_id = fields.Many2many('product.public.category', string='Category', related='product_id.public_categ_ids')
    parent_id = fields.Many2one('res.partner', string='Company', related='pdt_requirement.partner_id')
    partner_id = fields.Many2one('res.partner', string='Submitter', default=lambda self: self.env.user.partner_id)
    currency_id = fields.Many2one('res.currency', string='Currency', related='pdt_requirement.currency_id')
    uom_id = fields.Many2one('product.uom', string='Unit', related='pdt_quote.uom_id')
    uom_qty = fields.Float(string='Quantity', related='pdt_quote.uom_qty')
    seller_ids = fields.One2many('product.supplierinfo', 'product_id', string='Supplier Pricelist')
    market_price = fields.Float(string='Market Price', compute='_compute_unit')
    price_unit = fields.Float(string='Supplier Price', compute='_select_supplier')
    price_tax = fields.Float(string='Tax Cost', compute='_compute_unit')
    cost_price = fields.Float(string='Cost with Tax', compute='_compute_unit')
    cost_total = fields.Float(string='Total cost without Tax', compute='_compute_cost')
    cost_tax_total = fields.Float(string='Total cost with Tax', compute='_compute_cost')
    margin = fields.Float(string='Margin', compute='_compute_cost')
    tax_id = fields.Many2many('account.tax', string='Taxes', related='product_id.supplier_taxes_id')
    supplier_currency_id = fields.Many2one('res.currency', string='Supplier Currency', compute='_select_supplier')
    supplier_uom = fields.Many2one('product.uom', string='Supplier Uom', compute='_select_supplier')
    delay = fields.Float(string='Purchase Delay', compute='_select_supplier')
    price_total = fields.Float(string='Sale Price Total', compute='_compute_total')
    cost_total_currency = fields.Float(string='Cost with Currency', compute='_compute')
    price_total_currency = fields.Float(string='Sale Price with Currency', compute='_compute')
    price_unit_currency = fields.Float(string='Unit Cost with Currency', compute='_compute')
    user_id = fields.Many2one('res.users', string='Manager')
    market_price_currency = fields.Float(string='Sale Price', compute='_compute')
    price_rate = fields.Float(string='Price Rate')
    valid_date = fields.Date(string='Valid Date', compute='_select_supplier')
    complete_name = fields.Char(string='Name', compute='_compute_complete_name', store=True)

    _sql_constraints = [
        ('complete_name_uniq', 'unique (complete_name)', "Product already exists!"),
    ]

    @api.depends('product_id')
    def _compute_complete_name(self):
        for category in self:
            category.complete_name = '%s / %s' % (category.pdt_requirement.id, category.product_id.id)

    # 通过汇率计算价格
    @api.onchange('market_price', 'currency_id', 'supplier_currency_id')
    @api.depends('market_price', 'currency_id', 'supplier_currency_id')
    def _compute(self):
        for order in self:
            if order.currency_id and order.supplier_currency_id:
                order.price_unit_currency = self.env['res.currency']._compute(to_currency=order.currency_id,
                                                                              from_currency=order.supplier_currency_id,
                                                                              from_amount=order.price_unit)
                order.cost_total_currency = self.env['res.currency']._compute(to_currency=order.currency_id,
                                                                              from_currency=order.supplier_currency_id,
                                                                              from_amount=order.cost_total)
                order.market_price_currency = self.env['res.currency']._compute(to_currency=order.currency_id,
                                                                                from_currency=order.supplier_currency_id,
                                                                                from_amount=order.market_price)
                order.price_total_currency = self.env['res.currency']._compute(to_currency=order.currency_id,
                                                                               from_currency=order.supplier_currency_id,
                                                                               from_amount=order.price_total)

    @api.one
    def btn_display(self):
        self.user_id = self.env.uid

    @api.multi
    def btn_hide(self):
        for s in self:
            s.user_id = 0

    # 计算毛利与成本
    @api.depends('uom_qty')
    @api.onchange('uom_qty')
    def _compute_cost(self):
        for line in self:
            line.tax_total = line.price_tax * line.uom_qty
            line.cost_total = line.price_unit * line.uom_qty
            line.cost_tax_total = line.cost_price * line.uom_qty
            line.margin = line.price_total - line.cost_total - line.tax_total

    # 计算人民币总价
    @api.depends('uom_qty', 'market_price', 'product_id')
    def _compute_total(self):
        for line in self:
            price_total = line.market_price * line.uom_qty
            line.update({
                'price_total': price_total,
            })

    # 计算单价，免税价
    @api.onchange('price_unit', 'tax_id', 'product_id', 'price_rate', 'parent_id')
    @api.depends('price_unit', 'tax_id', 'product_id', 'price_rate', 'parent_id')
    def _compute_unit(self):
        for line in self:
            market_price = line.price_unit * (1 / (1 - line.product_id.compute_price_rate(product_id=line.product_id,
                                                                                          partner_id=line.parent_id,
                                                                                          price_rate=line.price_rate)))
            taxes = line.tax_id.compute_all(line.price_unit, line.currency_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'cost_price': taxes['total_included'],
                'market_price': market_price,
            })

    # 通过供应商价格表获取成本价
    @api.onchange('partner_id', 'uom_qty', 'create_date')
    @api.depends('partner_id', 'uom_qty', 'create_date')
    def _select_supplier(self):
        for s in self:
            for product in s.product_id:
                supplier = product._select_seller(quantity=s.uom_qty, date=s.create_date, uom_id=s.uom_id)
                s.price_unit = supplier.price
                s.supplier_currency_id = supplier.currency_id
                s.supplier_uom = supplier.product_uom
                s.delay = product.sale_delay
                s.valid_date = supplier.date_end

    # 添加到Purchase plan的产品信息
    @api.multi
    def cycle_project_product_append(self):
        context = {
            'default_product_id': self.product_id.id,
            'default_description': self.name,
            'default_so_currency_id': self.currency_id.id,
            'default_quotation_id': self.pdt_quote.id,
            'default_daily_cost': self.pdt_quote.daily_cost,
        }
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'quotation.product.line.append.br',
                'target': 'new',
                'context': context,
                }

    @api.multi
    def view_product_pricing(self):
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'quotation.product.line',
                'target': 'new',
                'res_id': self.id,
                }

    @api.multi
    def view_product_infor(self):
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'product.product',
                'target': 'current',
                'res_id': self.product_id.id,
                }

    # 选择为Quotation产品
    @api.multi
    def apply_product(self):
        self.pdt_quote.write({
            'product_chose': self.id,
            'state': 'green',
        })


class quotation_tags(models.Model):
    _name = 'quotation.tags'
    _description = 'Tags for quotation'

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    requirements = fields.Text('Requirements',
                               help="Enter here the internal requirements for this stage (ex: Offer sent to customer). It will appear as a tooltip over the stage's name.")
    color = fields.Integer(string='Color Index', default=10)


class ApplicationTags(models.Model):
    _name = 'product.application'
    _description = 'Tags for Product'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'complete_name'
    _order = 'parent_left'

    name = fields.Char(string='Application')
    color = fields.Integer(string='Color Index', default=10)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('product.application', 'Parent Category', index=True, ondelete='cascade')
    child_id = fields.One2many('product.application', 'parent_id', 'Child Categories')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name


class product_quotation(models.Model):
    _name = 'product.quotation'
    _description = 'Quotation Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, translate=True)
    default_code = fields.Char(string='Inquiry Code')
    application = fields.Many2many('product.application', string='Application', compute='_compute_application')
    function = fields.Char(string='Function')
    create_date = fields.Date(string='Date', default=fields.Date.today())
    requirement_id = fields.Many2one('sale.requirement', string='Quotation', ondeldete='cascade')
    description = fields.Text(string='Department Requirement', compute='_compute_require_description')
    customer_description = fields.Text(string='Customer Description')
    categ_id = fields.Many2one('product.public.category', string='Category')
    customer_image = fields.Binary(string='Image', attachment=True)
    customer_images = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'product.quotation')],
                                      string="Attachments")
    product_ref = fields.Char(string='Quotation NO.',
                              default=lambda self: self.env['ir.sequence'].next_by_code('product.quotation'))
    uom_qty = fields.Float(string='Order Quantity', track_visibility='onchange', compute='_compute_qty_quotation_')
    uom_id = fields.Many2one('product.uom', string='Unit', required=True)
    user_id = fields.Many2one('res.users', string='SCM-User')
    country_policy = fields.Text(string='Country Policy')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.requirement_id.currency_id)
    fuction_standard = fields.Text(string='Fuction Standard')
    is_standard = fields.Boolean(string='Standard', default=True)
    customized_description = fields.Text(string='Description for Customized')
    product_line = fields.One2many('quotation.product.line', 'pdt_quote', string='Product', copy=True)
    product_chose = fields.Many2one('quotation.product.line', string='Product', copy=True)
    supplier_name = fields.Many2one('res.partner', string='Supplier', related='product_id.supplier_name', store=True)
    product_id = fields.Many2one('product.product', string='Product', related='product_chose.product_id')
    customer_id = fields.Many2one('res.partner', string='Submitter', default=lambda self: self.env.user.partner_id)
    parent_id = fields.Many2one('res.partner', string='Company', related='requirement_id.partner_id')
    customer_barcode = fields.Char(string='Customer Ref')
    department = fields.Many2many('res.department', string='Department', compute='_compute_department')
    subtotal = fields.Float(string='Subtotal', related='product_chose.price_total_currency')
    color = fields.Integer(string='Color Index', default=10, compute="change_colore_on_kanban")
    department_line_ids = fields.One2many('res.department.line', 'product_quot_id', string='Department')
    product_star = fields.Integer('Star Rating', related='requirement_id.product_star')
    amount = fields.Float(string='Store Amount', compute='_compute_stock_amount')
    purchase_amount = fields.Float(string='Safety Stock')

    month_stock = fields.Float(string='Monthly Stock', compute='_number_of_monthly_amount')
    month_in_count = fields.Integer(string='Monthly Stock Order', compute='_number_of_monthly_in_count')
    month_comsumption = fields.Float(string='Monthly Usage', compute='_number_of_monthly_amount')
    month_out_count = fields.Integer(string='Monthly Usage Order', compute='_number_of_monthly_usage_count')
    total_comsumption = fields.Float(string='Yearly Usage', compute='_number_of_year_comsumption')
    total_stock = fields.Float(string='Yearly Stock', compute='_number_of_year_stock')

    state = fields.Selection([
        ('black', 'Pending'),
        ('green', 'Approved'),
    ], string='State', default='black', required=True)

    # 添加到Purchase plan的产品信息
    @api.multi
    def product_stock_add(self):
        context = {
            'default_product_quot_id': self.id,
            'default_product_id': self.product_id.id,
            'default_state': '1',
            'default_work_type': '1',
        }
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'res.department.stock.line',
                'target': 'new',
                'context': context,
                }

    @api.multi
    def product_stock_decrease(self):
        context = {
            'default_product_quot_id': self.id,
            'default_product_id': self.product_id.id,
            'default_state': '1',
            'default_work_type': '2',
        }
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'res.department.stock.line',
                'target': 'new',
                'context': context,
                }

    @api.depends('amount')
    def _number_of_monthly_usage_count(self):
        for s in self:
            domain = [('product_quot_id', '=', s.id),
                      ('work_type', '=', '2'),
                      ('state', '=', '1'),
                      ('month', '=', datetime.today().strftime('%m')),
                      ('year', '=', datetime.today().strftime('%Y')),
                      ]
            s.month_out_count = len(s.env['res.department.stock.line'].search(domain).ids)

    @api.depends('amount')
    def _number_of_monthly_in_count(self):
        for s in self:
            domain = [('product_quot_id', '=', s.id),
                      ('work_type', '=', '1'),
                      ('state', '=', '1'),
                      ('month', '=', datetime.today().strftime('%m')),
                      ('year', '=', datetime.today().strftime('%Y')),
                      ]
            s.month_in_count = len(s.env['res.department.stock.line'].search(domain).ids)

    @api.one
    def _compute_stock_amount(self, total_comsumption=0.0, total_stock=0.0):
        domain1 = [('product_quot_id', '=', self.id),
                   ('work_type', '=', '2'),
                   ('state', '=', '2'),
                   ]
        for amount in self.env['res.department.stock.line'].search(domain1):
            total_comsumption += amount.amount
        domain2 = [('product_quot_id', '=', self.id),
                   ('work_type', '=', '1'),
                   ('state', '=', '2'),
                   ]
        for amount in self.env['res.department.stock.line'].search(domain2):
            total_stock += amount.amount
        self.amount = total_stock - total_comsumption

    @api.depends('amount')
    def _number_of_monthly_amount(self):
        for s in self:
            domain = [('product_quot_id', '=', s.id),
                      ('work_type', '=', '2'),
                      ('state', '=', '2'),
                      ('month', '=', datetime.today().strftime('%m')),
                      ('year', '=', datetime.today().strftime('%Y')),
                      ]
            for amount in s.env['res.department.stock.line'].search(domain):
                s.month_comsumption += amount.amount
            domain2 = [('product_quot_id', '=', s.id),
                       ('work_type', '=', '1'),
                       ('state', '=', '2'),
                       ('month', '=', datetime.today().strftime('%m')),
                       ('year', '=', datetime.today().strftime('%Y')),
                       ]
            for amount in s.env['res.department.stock.line'].search(domain2):
                s.month_stock += amount.amount

    @api.depends('amount')
    def _number_of_year_comsumption(self):
        for s in self:
            domain = [('product_quot_id', '=', s.id),
                      ('work_type', '=', '2'),
                      ('state', '=', '2'),
                      ('year', '=', datetime.today().strftime('%Y')),
                      ]
            for amount in s.env['res.department.stock.line'].search(domain):
                s.total_comsumption += amount.amount

    @api.depends('amount')
    def _number_of_year_stock(self):
        for s in self:
            domain = [('product_quot_id', '=', s.id),
                      ('work_type', '=', '1'),
                      ('state', '=', '2'),
                      ('year', '=', datetime.today().strftime('%Y')),
                      ]
            for amount in s.env['res.department.stock.line'].search(domain):
                s.total_stock += amount.amount

    @api.depends('department_line_ids')
    @api.onchange('department_line_ids')
    def _compute_department(self):
        self.department = self.department_line_ids.mapped('department_id')

    @api.depends('department_line_ids')
    @api.onchange('department_line_ids')
    def _compute_application(self):
        self.application = self.department_line_ids.mapped('application')

    @api.one
    def btn_claim(self):
        self.user_id = self.env.uid

    @api.one
    def need_customized(self):
        for s in self:
            s.is_standard = not s.is_standard
            s.color = 11
            return True

    @api.multi
    def btn_refuse_claim(self):
        for s in self:
            s.user_id = 0

    @api.depends('department_line_ids')
    def _compute_qty_quotation_(self):
        for q in self:
            if q.department_line_ids:
                for value in q.department_line_ids:
                    q.uom_qty += value.values

    @api.depends('state')
    @api.onchange('state')
    def change_colore_on_kanban(self):
        for record in self:
            color = 0
            if record.state == 'red':
                color = 0
            elif record.state == 'green':
                color = 7
            record.color = color

    @api.depends('department_line_ids')
    def _compute_require_description(self):
        for required in self:
            variant = ''
            for item in required.department_line_ids:
                name = ''
                for dept in item.department_id:
                    name += (str(dept.name) + ',')
                if item.application:
                    variant += ('(' + str(name) + ')' + str(item.application.name) + ' : ' + str(item.values) + '\n')
                else:
                    variant += (str(name) + ' : ' + str(item.values) + '\n')
            required.description = variant or required.name


class RequirementTags(models.Model):
    _name = 'requirement.tags'
    _description = 'Tags for requirement'

    name = fields.Char(string='Style')
    color = fields.Integer(string='Color Index', default=10)
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class QuotationTags(models.Model):
    _name = 'scenario.tags'
    _description = 'Tags for scenario'

    name = fields.Char(string='State')
    color = fields.Integer(string='Color Index', default=10)
    description = fields.Text(string='Description')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class sale_quotation(models.Model):
    _name = 'sale.requirement'
    _description = 'Requirement Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True)
    image = fields.Binary(string='Image', related='partner_id.image')
    order_ref = fields.Char(string='Requirement NO.',
                            default=lambda self: self.env['ir.sequence'].next_by_code('requirement.inquiry'))
    quote_line = fields.One2many('product.quotation', 'requirement_id', string='Quote Product', copy=True)
    order_id = fields.Many2one('sale.order', string='Sale Order')
    number_of_quote = fields.Integer(string='Quot.', compute='_number_of_quote')
    number_of_unsure = fields.Integer(string='Quot.', compute='_number_of_unsure')
    project_manager = fields.Many2one('res.users', string='Project Manager', ondelete='set null', index=True,
                                      default=lambda self: self.partner_id.user_id)
    scenario_id = fields.Many2many('scenario.tags', string='Scenario', copy=True)
    partner_id = fields.Many2one('res.partner', string='Company', index=True, related="staff_id.parent_id")
    barcode = fields.Char(string='Customer Code', related='partner_id.barcode')
    description = fields.Text(string='Project Description')
    total_budget = fields.Float(string='Total Budget', compute='_total_budget')
    product_line = fields.One2many('quotation.product.line', 'pdt_requirement', string='Product List', copy=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    price_rate = fields.Float(string='Price Rate', related='partner_id.price_rate')
    currency_id = fields.Many2one('res.currency', required=True)
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    start_schedule = fields.Date(string='Estimated opening time')
    hotel_style = fields.Many2many('requirement.tags', string='Hotel Style', copy=True)
    response_schedule = fields.Date(string='Expected quotation time', track_visibility='onchange')
    build_area = fields.Float(string='Building Area')
    staff_id = fields.Many2one('res.partner', track_visibility='onchange', string='Initiator',
                               default=lambda self: self.env.user.partner_id)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'sale.requirement')],
                                     string="Attachments")
    product_star = fields.Integer(string='Star Rating')
    state = fields.Selection([
        ('red', 'Pending'),
        ('green', 'Completed')], string='State', default='red', required=True)
    sale_order_count = fields.Integer(string='Order Count', compute='_number_of_order')
    plan_count = fields.Integer(string='Plan Count', compute='_number_of_plan')
    product_count = fields.Integer(string='Product Count', compute='_number_of_pricing')

    # 计算订单数量
    @api.depends()
    def _number_of_pricing(self):
        for s in self:
            domain = [('requirement_id', '=', s.id), ('product_chose', '!=', None)]
            count = len(s.env['product.quotation'].search(domain).ids)
            s.product_count = count

    # 计算订单数量
    @api.depends()
    def _number_of_plan(self):
        for s in self:
            domain = [('requirement_id', '=', s.id)]
            count = len(s.env['quotation.cycle'].search(domain).ids)
            s.plan_count = count

    # 计算订单数量
    @api.depends()
    def _number_of_order(self):
        for s in self:
            domain = [('requirement_id', '=', s.id)]
            count = len(s.env['sale.order'].search(domain).ids)
            s.sale_order_count = count

    # 计算询盘数量
    @api.depends()
    def _number_of_quote(self):
        for s in self:
            domain = [('requirement_id', '=', s.id)]
            count = len(s.env['product.quotation'].search(domain).ids)
            s.number_of_quote = count

    # 计算询盘数量
    @api.depends()
    def _number_of_unsure(self):
        for s in self:
            domain = [('requirement_id', '=', s.id), ('product_chose', '=', None)]
            count = len(s.env['product.quotation'].search(domain).ids)
            s.number_of_unsure = count

    # 计算总预算
    @api.multi
    def _total_budget(self):
        for sale in self:
            sale.total_budget = 0
            for line in sale.quote_line:
                sale.total_budget += line.subtotal

    @api.one
    def _cancel_order(self):
        if self.order_id.state == 'sale':
            warning_message = "This order was confirmed!"
            raise Warning(warning_message)
        else:
            self.state = 'red'
            return self.order_id.action_cancel

    # 创建订单
    def action_create_order_new(self):
        self.state = 'green'
        vals = {'partner_id': self.partner_id.id,
                'user_id': self.project_manager.id,
                'requirement_id': self.id,
                }
        sale_order = self.env['sale.order'].create(vals)
        self.order_id = sale_order.id
        order_line = self.env['sale.order.line']
        domain = [('product_chose', '!=', None)]
        line = self.env['product.quotation'].search(domain)
        product = line.product_chose
        description = "Product Description:" + '\n'
        if line.description:
            description = description + str(line.description) + '\n'
        if line.customer_description:
            description = description + str(line.customer_description) + '\n'
        if line.country_policy:
            description = description + str(line.country_policy) + '\n'
        if line.fuction_standard:
            description = description + str(line.fuction_standard) + '\n'
        if line.customized_description:
            description = description + str(line.customized_description) + '\n'
        pdt_value = {
            'order_id': sale_order.id,
            'product_id': product.product_id.id,
            'quotation_id': line.id,
            'product_uom': line.uom_id.id,
            'price_unit': product.market_price,
            'name': description,
            'customer_lead': product.delay,
            'product_chosen': line.product_chose,
        }
        order_line.create(pdt_value)
        view_id = self.env.ref('sale.view_order_form')
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': sale_order.id,
            'view_id': view_id.id,
        }

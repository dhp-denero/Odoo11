# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime
from datetime import datetime


class res_department(models.Model):
    _name = 'res.department'
    _description = 'Department Management'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    description = fields.Text('Description', translate=True)
    color = fields.Integer(string='Color Index', default=10)
    parent_id = fields.Many2one('res.department', 'Superior', index=True, ondelete='cascade')
    child_id = fields.One2many('res.department', 'parent_id', 'Subordinate')
    parent_left = fields.Integer('Left Parent', index=1)
    parent_right = fields.Integer('Right Parent', index=1)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class QuotationDepartmentLine(models.Model):
    _name = 'res.department.line'
    _rec_name = 'complete_name'

    @api.model
    def _search_my_department(self):
        dept = self.env.user.department.ids
        return [('id', 'child_of', dept)]

    @api.model
    def _search_my_application(self):
        app = self.env.user.application.ids
        return [('id', 'child_of', app)]

    product_quot_id = fields.Many2one('product.quotation', 'Quotation', ondelete='cascade', required=True)
    product_id = fields.Many2one('quotation.product.line', string='Selected Product', related='product_quot_id.product_chose')
    requirement_id = fields.Many2one('sale.requirement', 'Requirement', related='product_quot_id.requirement_id')
    department_id = fields.Many2one('res.department', 'Department', ondelete='set null', domain=_search_my_department)
    values = fields.Float(string='Request Number')
    parent_id = fields.Many2one('res.partner', string='Company', related='partner_id.parent_id')
    partner_id = fields.Many2one('res.partner', string='Name', default=lambda self: self.env.user.partner_id)
    daily_cost = fields.Float(string='Daily Usage', default=1.0)
    description = fields.Char(string='Description')
    application = fields.Many2one('product.application', string='Application', domain=_search_my_application)
    date = fields.Date(string='Purchase Date on Schedule')
    complete_name = fields.Char(string='Name', compute='_compute_complete_name', store=True)

    _sql_constraints = [
        ('complete_name_uniq', 'unique (complete_name)', "Request already exists!"),
    ]

    @api.depends('product_id')
    def _compute_complete_name(self):
        for category in self:
            if category.department_id:
                category.complete_name = '%s / %s / %s' % (category.department_id.name, category.application.name, category.product_quot_id.name)
            else:
                category.complete_name = category.product_id.name


class StockLineAction(models.Model):
    _name = 'res.department.stock.line'
    _rec_name = 'product_quot_id'

    @api.model
    def _search_my_department(self):
        dept = self.env.user.department.ids
        return [('id', 'child_of', dept)]

    @api.model
    def _search_my_application(self):
        app = self.env.user.application.ids
        return [('id', 'child_of', app)]

    partner_id = fields.Many2one('res.partner', string='Submitter', default=lambda self: self.env.user.partner_id)
    parent_id = fields.Many2one('res.partner', string='Company', related='partner_id.parent_id')
    product_id = fields.Many2one('product.product', string='Product')
    product_quot_id = fields.Many2one('product.quotation', string='Quotation')
    amount = fields.Float(string='Amount')
    uom_id = fields.Many2one('product.uom', string='Unit', related='product_quot_id.uom_id')
    work_type = fields.Selection([('1', 'In'), ('2', 'Out')], string='Work Type')
    date = fields.Date(string='Create Date', default=fields.Date.today())
    state = fields.Selection([('1', 'Pending'), ('2', 'Finished'), ('3', 'Cancelled')], default='1', string='State')
    name = fields.Char(string='Description')
    month = fields.Integer(string='Month', compute='_compute_year_month', store=True)
    year = fields.Integer(string='Year', compute='_compute_year_month', store=True)
    application = fields.Many2one('product.application', string='Application', domain=_search_my_application)
    department_id = fields.Many2one('res.department', 'Department', ondelete='set null', domain=_search_my_department)

    # 出库
    @api.one
    def out_stock(self):
        if self.work_type == '1':
            stock = self.product_quot_id
            amount = stock.amount + self.amount
            self.state = '2'
            stock.write({
                'amount': amount
            })
        if self.work_type == '2':
            stock = self.product_quot_id
            amount = stock.amount - self.amount
            self.state = '2'
            stock.write({
                'amount': amount
            })

    @api.depends('date')
    @api.onchange('date')
    def _compute_year_month(self):
        for s in self:
            s.month = datetime.strptime(s.date, '%Y-%m-%d').strftime('%m')
            s.year = datetime.strptime(s.date, '%Y-%m-%d').strftime('%Y')

    @api.one
    def not_approve(self):
        self.state = '3'

    @api.one
    def confirm(self):
        pass

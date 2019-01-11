# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp

class WorkSheet(models.Model):
    """工作单"""

    _name = "work_sheet"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "work sheet including good ship operation infomation"
    _table = "work_sheet"
    _rec_name = "name"

    # @api.multi
    # def _get_in_out(self):
    #     for work_sheet in self:
    #         work_sheet.business_type.in_out

    # 基本信息
    name = fields.Char(string='Work Sheet ID', required=True, copy=False, state={'draft': [('readonly', False)]},
                       default=lambda self: _('New'))
    business_type = fields.Many2one(comodel_name="business_type", string="Business Type")
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
    contact = fields.Many2one(comodel_name="res.partner", string="Contact")
    source_type = fields.Selection(selection=[('pointed', 'Pointed'), ('seize', 'Seize')], string="SourceType")
    sale_order = fields.Many2one(comodel_name="sale.order", string="Sale Order", ondelete='set null')
    customer_internal_num = fields.Char(string='CustomerInnerNO', size=100)

    is_sea = fields.Boolean(string="Sea Shipping")
    is_air = fields.Boolean(string="Air Transport")
    is_land = fields.Boolean(string="Land Transport")
    is_warehouse = fields.Boolean(string="Warehouse")
    is_custom = fields.Boolean(string="Custom")

    # 货运信息
    cn_name = fields.Char(string="Chinese Name")
    en_name = fields.Char(string="English Name")
    marks = fields.Char(string='Marks')
    qty = fields.Integer(string='Qty')
    wrap_type = fields.Many2one(comodel_name='delegate_packing', string='Wrap Type')
    gross_weight = fields.Float(string='GrossWeight', digits=dp.get_precision('Stock Weight'))
    volume = fields.Float(string='Volume', digits=dp.get_precision('Stock Weight'))
    charge_weight = fields.Float(string='Charge Weight', digits=dp.get_precision('Stock Weight'))

    # 发运信息
    consignor = fields.Many2one(comodel_name='res.partner', string='Consignor', domain=[('is_company', '=', True)])
    input_company = fields.Many2one(comodel_name='res.partner',
                                      string='Input Company',
                                      domain=[('is_company', '=', True)])
    consignee = fields.Many2one(comodel_name='res.partner',
                                  string='Consignee',
                                  domain=[('is_company', '=', True)])
    overseas_agent = fields.Many2one(comodel_name='res.partner',
                                     string='Overseas Agent',
                                     domain=[('is_company', '=', True)])

    # 操作信息
    sale_man = fields.Many2one(comodel_name='res.users', string='Saler')
    customer_service = fields.Many2one(comodel_name='res.users', string='Customer Service')
    creater = fields.Many2one(comodel_name='res.users', string='Creater', readonly=True,
                              default=lambda self: self.env.user)
    creat_time = fields.Datetime(string='Create Time', readonly=True, default=fields.Datetime.now, required=True)

    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('done', 'Done'),
                                        ('cancle', 'Cancle')], string='status', readonly=True, default='draft')

    # 其它相关字段
    custom_declaration_draft = fields.One2many(comodel_name='custom_declaration_draft',
                                               inverse_name='work_sheet',
                                               string='Custom Declaration Draft')
    custom_count = fields.Integer(string='Custom Declaration NO', compute='_get_custom_count')
    # in_out = fields.Selection(string='InOut', selection=[('i', 'import'), ('e', 'export')],
    #                           compute=)

    @api.depends('custom_declaration_draft')
    def _get_custom_count(self):
        for sheet in self:
            sheet.custom_count = len(sheet.custom_declaration_draft)

    @api.multi
    def custom_declaration_view(self):
        """返回相关连的报关单"""

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'custom_declaration_draft',
            'view_mode': 'tree,form',
            'res_id': self.custom_declaration_draft.ids,
        }

        return action

    @api.multi
    def custom_book(self):
        """订舱"""
        pass

    @api.multi
    def complete(self):
        self.write({
            'state': 'done'
        })
        return True

    @api.multi
    def cancled(self):
        self.write({
            'state': 'cancle'
        })

        return True

    @api.multi
    def recover(self):
        self.write({
            'state': 'draft'
        })

        return True

    @api.model
    def create(self, vals):
        """设置命名和业务类型"""

        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work_sheet') or _('New')

        # 设置默认的业务类型
        business_type = self.env.context.get('set_business_type')
        if business_type:
            type_xml_id = 'service_center.business_type_for_' + business_type
            type_obj = self.env.ref(type_xml_id)
            vals['business_type'] = type_obj.id
        result = super(WorkSheet, self).create(vals)

        return result

    # # 增加工作单与报关单的一对一约束
    # @api.constrains('custom_declaration_draft')
    # def _check_custom_declaration_size(self):
    #     for work_sheet in self:
    #         if len(work_sheet.custom_declaration_draft) > 1:
    #             raise ValidationError(_('work sheet must hava most one custom declaration'))


class CustomDeclarationDraft(models.Model):
    """报关原始清单"""

    _name = 'custom_declaration_draft'
    _description = 'custom declaration related work sheet'
    _table = 'custom_declaration_draft'
    _rec_name = "name"

    def _get_business_company(self):

        if self.work_sheet.business_type.in_out == 'i':
            business_company = self.work_sheet.consignee
        elif self.work_sheet.business_type.in_out == 'e':
            business_company = self.work_sheet.consignor
        else:
            business_company = False

        return business_company

    in_out = fields.Selection(string='InOut', selection=[('i', 'import'), ('e', 'export')])     # 进出口类型
    port_code = fields.Many2one(comodel_name='delegate_customs', string='PortCode')             # 进出口岸
    transport_mode = fields.Many2one(comodel_name='delegate_transport_mode', string='Transport Mode')   # 运输方式
    trade_mode = fields.Many2one(comodel_name='delegate_trade_mode', string='Trade Mode')               # 监管方式
    duty = fields.Many2one(comodel_name='delegate_exemption', string='Duty')                    # 免征性质
    trade_country = fields.Many2one(comodel_name='delegate_country', string='Trade Country')    # 贸易国别
    deal_type = fields.Many2one(comodel_name='delegate_trade_terms', string='Deal Type')        # 成交方式
    nation = fields.Many2one(comodel_name='delegate_country', string='Nation')                  # 启运/抵达国
    haven = fields.Many2one(comodel_name='delegate_port', string='Haven')                       # 装货/指运港
    region = fields.Many2one(comodel_name='delegate_region', string='Region')                   # 境内货源/目的地
    qty = fields.Integer(string='Qty')
    wrap_type = fields.Many2one(comodel_name='delegate_packing', string='Wrap Type')            # 包装方式
    gross_weight = fields.Float(string='Gross Weight', digits=dp.get_precision('Stock Weight'))
    net_weight = fields.Float(string='Net Weight', digits=dp.get_precision('Stock Weight'))
    marks = fields.Char(string='Marks')
    remark = fields.Char(string='Remark')
    customs_declaration_num = fields.Char(string='Customs Declaration NO')
    customs_inspection_num = fields.Char(string='Customs Inspection NO')

    # 列表视图关联字段
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
    input_company = fields.Many2one(comodel_name='res.partner', string='input_company')
    business_type = fields.Many2one(comodel_name="business_type", string="Business Type",)
    state = fields.Selection(string='Status', selection=[('u', 'Unsent'), ('s', 'sent')], default='u', readonly=True)


    name = fields.Char(string='Custom Declaration Draft NO', required=True, copy=False,
                       state={'draft': [('readonly', False)]},
                       default=lambda self: _('New'))
    creater = fields.Many2one(comodel_name='res.users', string='Creater', default=lambda self: self.env.user)
    create_time = fields.Datetime(string='Create Time', readonly=True, default=fields.Datetime.now)
    business_company = fields.Many2one(comodel_name='res.partner', string='Business Company',
                                       default=_get_business_company)

    # 关联工作单和委托商品
    work_sheet = fields.Many2one(comodel_name='work_sheet', string='Work Sheet ID')  # 工作单号
    work_sheet_goods = fields.Many2one(comodel_name='work_sheet_good', string='Work sheet goods')


    @api.model
    def create(self, vals):
        """设置命名"""

        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('work_sheet') or _('New')

        result = super(CustomDeclarationDraft, self).create(vals)

        return result

    @api.multi
    def send(self):
        """发送报文"""

        self.write({'state': 's'})

        return True

    @api.onchange('work_sheet')
    def _onchange_work_sheet(self):

        if not self.work_sheet:
            return
        work_sheet = self.work_sheet
        self.customer = work_sheet.customer
        self.in_out = work_sheet.business_type.in_out
        self.transport_mode = work_sheet.business_type.transport_mode
        self.input_company = work_sheet.input_company
        self.qty = work_sheet.qty





class WorkSheetGood(models.Model):
    """委托商品信息"""

    _name = 'work_sheet_good'
    _description = 'work sheet goods for work sheet and custom declaration'
    _table = 'work_sheet_good'

    work_sheet_ID = fields.Char(string='WorkSheetID')
    hs_code = fields.Many2one(comodel_name='product_hs_code', string='HS Code')
    cn_name = fields.Char(raleted='hs_code.G_Name', string='Chinese Name')
    en_name = fields.Char(string='English Name')
    model = fields.Char(string='Model')
    deal_qty = fields.Integer(string='Deal Qty')
    deal_unit = fields.Many2one(comodel_name='turnover_unit', string='Deal Unit')
    deal_unit_price = fields.Float(string='Deal Unit Price', digits=dp.get_precision('Product Price'))
    deal_amount = fields.Float(string='Deal Amount', digits=dp.get_precision('Product Price'))
    currency = fields.Many2one(comodel_name='currency_system', string='Currency')
    origin_country = fields.Many2one(comodel_name='delegate_country', string='Origin Country')

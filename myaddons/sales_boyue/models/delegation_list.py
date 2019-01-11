# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .. import utils

class Delegation_list(models.Model):
    """委托清单"""
    _name = 'delegation_list'
    _description = 'a delegation_list for sale order'
    _rec_name = 'contract_num'

    contract_num = fields.Char('合同号')
    contact_person = fields.Many2one('res.partner', string='联系人', compute='_get_contact_person')   # 联系人要为客户公司的联系人
    sender = fields.Many2one('res.partner', string='发货人')
    import_and_export = fields.Selection(
        [('i', '进口'), ('e', '出口')],
        '进出口类型',
        # required=True
    )
    transport = fields.Many2one('delegate_transport_mode', '运输方式')
    exemption = fields.Many2one('delegate_exemption', '免征性质')
    trade_term = fields.Many2one('delegate_trade_terms', '成交方式')
    port = fields.Many2one('delegate_port', '装货/指运港')
    num = fields.Integer('件数')
    gross_weight = fields.Float('毛重')
    mark_code = fields.Char('标记唛码')
    remarks = fields.Text('备注')
    seller = fields.Many2one('res.partner', string='销售员')   # 暂时写为所有员工，以后要改为客户下销售员

    delegate_company = fields.Many2one('res.partner', '委托单位')   # 委托单位为客户
    phone = fields.Char('联系人电话', related='contact_person.phone')  # 必须关联联系人字段，而且为只读
    Receiver = fields.Many2one('res.partner', string='收货人')
    customs = fields.Many2one('delegate_customs', string='进出口岸')
    trade_mode = fields.Many2one('delegate_trade_mode', string='监管方式')
    trade_country = fields.Many2one('delegate_country', string='贸易国别')
    origin_arrival_country = fields.Many2one('delegate_country', string='启运/抵达国')
    region = fields.Many2one('delegate_region', string='境内货源/目的地')
    packing = fields.Many2one('delegate_packing', string='包装方式')
    net_weight = fields.Float('净重')
    operator = fields.Many2one('res.users', string='操作员', default=lambda self:self.env.user.id)     # 操作员要关联当前登陆的用户



    sale_order = fields.Many2one('sale.order', string='销售订单')
    product_data_list = fields.One2many('delegate_product_data', 'product_list_id', string='商品列表')
    amount_total = fields.Float('总计', compute='_get_amount_total')
    message = fields.Selection(
        [('0', '货代'),('1', '报关'),('2', '仓储')],
        '报文类型',
        default='1'
    )

    state = fields.Selection(
        [('unsent', '未发送'), ('sent', '已发送'), ('failed', '发送失败')],
        '发送状态',
        default='unsent',
        readonly=True
    )


    @api.multi
    def send_data(self):
        self.ensure_one()
        delegation_list_send = self.env['delegation_list_send']
        delegation_list_send_dic = {

        }
        # utils.to_xml.delegate_to_xml(self)
        utils.to_json.delegation_to_json(self)
        print('---------------- has send -------------------')


    @api.depends('sale_order.amount_total')
    def _get_amount_total(self):
        for item in self:
            print(item.sale_order.amount_total)
            item.amount_total = item.sale_order.amount_total

    @api.depends('delegate_company')
    def _get_contact_person(self):
        for comapny in self:
            if comapny.delegate_company:
                if comapny.delegate_company.child_ids:
                    comapny.contact_person = comapny.delegate_company.child_ids[0]

    @api.depends('contact_person')
    def _get_contact_phone(self):
        for body in self:
            if body.contact_person:
                body.phone = body.contact_person.phone


class Delegation_list_send(models.Model):
    """已发送的委托清单"""
    _name = 'delegation_list_send'
    _description = 'a delegation_list for sale order has send'

    contract_num = fields.Char('合同号')
    import_and_export = fields.Char('进出口类型')
    port_cn = fields.Char('进出口岸')
    trade_mode_name = fields.Char("监管方式")
    trade_country_co = fields.Char("贸易国别")
    nation_co = fields.Char("启运/抵达国")
    haven_co = fields.Char("装货/指运港")
    partner_id = fields.Char('收发货人')
    sale_order = fields.Char('销售订单')
    product_data_list = fields.One2many('delegate_product_data_send', 'product_list_id', string='商品列表')
    amount_total = fields.Float('总计')



















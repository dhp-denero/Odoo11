# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Order(models.Model):
    """继承销售订单，添加通关数据字段"""
    _description = 'sale.order added some details about custom'
    _inherit = 'sale.order'

    # 进出口类型
    import_and_export = fields.Selection(
        [('i', '进口'), ('e', '出口')],
        '进出口类型',
        # required=True
    )
    transport = fields.Many2one('customs_basedata.delegate_transport_mode', string='Transport Mode')     # 运输方式
    exemption = fields.Many2one('customs_basedata.delegate_exemption', string='Exemption')               # 免征性质
    trade_term = fields.Many2one('customs_basedata.delegate_trade_terms', string='Trade Term')           # 成交方式
    port = fields.Many2one('customs_basedata.delegate_port', string='Port')                              # 装货/指运港
    num = fields.Integer('Num')                     # 件数
    gross_weight = fields.Float('Gross Weight')     # 毛重
    mark_code = fields.Char('Mark Code')            # 标记唛码
    remarks = fields.Text('Remarks')                # 备注

    customs = fields.Many2one('customs_basedata.delegate_customs', string='Custom')        # 进出口岸
    trade_mode = fields.Many2one('customs_basedata.delegate_trade_mode', string='Trade Mode')         # 监管方式
    trade_country = fields.Many2one('customs_basedata.delegate_country', string=' Country')         # 贸易国别
    origin_arrival_country = fields.Many2one('customs_basedata.delegate_country', string='启运/抵达国')
    region = fields.Many2one('customs_basedata.delegate_region', string='境内货源/目的地')
    packing = fields.Many2one('customs_basedata.delegate_packing', string='包装方式')
    net_weight = fields.Float('净重')
    delegate_id = fields.Many2one('delegation_list', string='委托清单名')

    @api.multi
    def create_delegation_list(self):
        """
        创建委托清单
        :return:
        """
        self.ensure_one()
        delegation_list = self.env['delegation_list']
        obj = delegation_list.search([('contract_num', '=', self.name)])

        #   查找对应的委托清单，如果没有就创建
        if not obj:
            dic = {
                'contract_num':self.name,
                'import_and_export':self.import_and_export,
                'transport': self.transport.id,
                'exemption': self.exemption.id,
                'trade_term': self.trade_term.id,
                'port': self.port.id,
                'num': self.num,
                'gross_weight': self.gross_weight,
                'mark_code': self.mark_code,
                'remarks': self.remarks,
                'delegate_company': self.partner_id.id,

                'customs': self.customs.id,
                'trade_mode': self.trade_mode.id,
                'trade_country': self.trade_country.id,
                'origin_arrival_country': self.origin_arrival_country.id,
                'region': self.region.id,
                'packing': self.packing.id,
                'net_weight': self.net_weight,
                'seller': self.seller.id,
            }
            obj = delegation_list.create(dic)

            self.ensure_one()
            # 遍历销售中的产品清单，获得委托清单中长品所需要的数据
            for order in self.order_line:
                product_id = order.product_id
                dic = {}

                # 产品中 hs_code, 规格型号, 原产国/目的国, 成交单位, 币种
                for key in ['hs_code', 'specifications', 'delegate_country', 'unit', 'currency']:
                    value = getattr(product_id, key)
                    if value:
                        dic[key] = getattr(value, 'id')

                # 订单线中 成交数量， 单价， 总价
                for key in ['qty_invoiced', 'price_unit', 'price_subtotal']:
                    value = getattr(order, key)
                    if value:
                        dic[key] = value
                print(dic)
                product_obj = self.env['delegate_product_data'].create(dic)
                obj.product_data_list |= product_obj

            self.delegate_id = obj.id


        return {
            'type': 'ir.actions.act_window',
            'res_model': obj._name,  # this model
            'res_id': obj.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
        }


    @api.model
    def create(self, vals):
        '''重新设计订单号的生成，加入进出口类型，运输方式，日期等参数'''

        if vals.get('name', _('New')) == _('New'):
            transport = self.env['delegate_transport_mode'].browse(vals['transport'])
            import_and_export = vals['import_and_export'].upper()

            import pytz
            tz = pytz.timezone('Asia/Shanghai')
            local_time = fields.datetime.now(tz).strftime('%Y%m%d')
            name = 'BYJC' + transport.Code + import_and_export + local_time
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
            vals['pricelist_id'] = vals.setdefault('pricelist_id',
                                                   partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(Order, self).create(vals)
        return result

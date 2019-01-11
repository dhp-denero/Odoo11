# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DevelopmentProgress(models.Model):
    _name = 'supplier.progress'

    name = fields.Char(string='Development Progress')

class PartnerTree(models.Model):
    _name = 'res.partner.contract'

    number = fields.Char(string='Text')
    note = fields.Char(string='Descritpion')
    partner_id = fields.Many2one('res.partner', string='Partner')
    type = fields.Many2one('contract.type', string='Contract type')

class ContractType(models.Model):
    _name = 'contract.type'

    name = fields.Char(string='Tag')



class PartnerAdvanced(models.Model):
    _inherit = 'res.partner'

    managementuser_id = fields.Char(string='资料账号')
    management_account = fields.Char(string='管理账号')
    brand = fields.Many2many('res.brand', string='Brand')
    stock_exist = fields.Selection([('yes', 'YES'),
                                  ('no', 'NO')], string='Stock Exist', default='no')
    develop_prog = fields.Many2many('supplier.progress', string='Supplier Develop Progress')
    # 公司网站
    x_1688 = fields.Char(string='1688.com')
    x_alibaba = fields.Char(string='Alibaba.com')
    x_tianyancha = fields.Char(string='Tianyancha')
    x_linkedinweb = fields.Char(string='LinkedIn.com')
    x_facebookweb = fields.Char(string='Facebook.com')
    x_twitterweb = fields.Char(string='Twitter.com')
    x_blogweb = fields.Char(string='Blog')
    # 已有字段公司
    x_cooperatoinstarts = fields.Date(string='Cooperation Date')
    x_cooperationways = fields.Char(string='Cooperation Description')
    x_commercial_company_name = fields.Char(string='Company Name')
    x_sc_paymentcycle = fields.Selection([('0天', 'Immdiately'),
                                          ('15天', '15 Days'),
                                          ('30天', '30 Days'),
                                          ('45天', '45 Days'),
                                          ('60天', '60 Days'),
                                          ('90天', '90 Days'),
                                          ('180天', '180 Days')], string='Payment Cycle')
    x_groupname = fields.Char(string='Group Name')
    x_sc_mainproductscn = fields.Text(string='Main Product（Chinese）')
    x_sc_mainproductsen = fields.Text(string='Main Product', translated=True)
    x_sc_productioncycle = fields.Char(string='Produce Cycle', translated=True)
    x_background = fields.Text(string='Background', translated=True)
    x_existence = fields.Selection([('在营', 'Opening'),
                                    ('注销', 'Cancellation'),
                                    ('停业', 'Closed'),
                                    ('清算', 'Liquidation')],
                                   string='Existence')
    x_turnover = fields.Char(string='Nearly three years turnover (USD / ten thousand)')
    x_dateofestablishment = fields.Date(string='Date of establishment')
    x_staffnumbers = fields.Char(string='Staff Counts')
    x_cityrating = fields.Integer(string='City Rating')
    x_area = fields.Char(string='Premises area(㎡)')
    x_structuretree = fields.Text(string='Organization')
    x_companycategory = fields.Selection([('股份', '股份'),
                                          ('有限', '有限'),
                                          ('合伙', '合伙'),
                                          ('个体户', '个体户'),
                                          ('个人独资', '个人独资'),
                                          ('合资', '合资'),
                                          ('外资', '外资')],
                                         string='Ownership')
    x_businesslicense = fields.Char(string='Business license')
    x_registrationaddress = fields.Char(string='Business Register Location')
    x_businessscope = fields.Char(string='Business Scope')
    x_legalrepresentative = fields.Char(string='Artificial Person')
    x_typeofregistration = fields.Char(string='Type of registration')
    x_registrationcapital = fields.Char(string='Registration Capital')
    x_registrationauthority = fields.Char(string='Registration Authority')
    x_trademark = fields.Char(string='Trademark')
    x_intellectualproperty = fields.Text(string='Intellectual property')
    x_taxpayertype = fields.Char(string='Tax payer type')
    x_sc_certificates = fields.Text(string='Certificates')
    x_sc_productionfacility = fields.Text(string='Production facility')
    x_sc_productioncapacity = fields.Char(string='Yearly output')
    x_sc_peaklowseasons = fields.Char(string='Peaklow Seasons')
    x_sc_supplierbigclients = fields.Char(string='Clients Information')
    x_sc_exportrights = fields.Selection([('是', 'YES'),
                                          ('否', 'NO')], string='Export Right')
    x_sc_exportpercentage = fields.Selection([('0%', '0%'),
                                              ('25%', '25%'),
                                              ('50%', '50%'),
                                              ('75%', '75%'),
                                              ('100%', '100%')], string='Export Per.')
    x_sc_pricerange = fields.Selection([('高', 'High'),
                                        ('中', 'Medium'),
                                        ('低', 'Low')], string='Price Range')
    x_sc_servicerange = fields.Selection([('好', 'Good'),
                                          ('中', 'Normal'),
                                          ('差', 'Bad')], string='Service')

    # 市场部
    x_mk_airbnbcom = fields.Char(string='Airbnb.com')
    x_mk_bookingcom = fields.Char(string='Booking.com')
    x_mk_ctripcom = fields.Char(string='Ctrip.com')
    x_mk_expediacom = fields.Char(string='Expedia.com')
    x_mk_homeawaycom = fields.Char(string='HomeAway.com')
    x_mk_qunaercom = fields.Char(string='Qunaer.com')
    x_mk_tripadvisorcom = fields.Char(string='Tripadvisor.com')
    x_mk_numberofoperatinghotels = fields.Char(string='Number of hotels')
    x_mk_numberofoperatingrestaurants = fields.Char(string='Number of Restaurants')
    x_mk_roomnumbers = fields.Char(string='Number of Rooms')
    x_mk_customertype = fields.Selection([('hotel', 'Hotel'),
                                          ('f&b', 'F&B'),
                                          ('apartment', 'Apartment'),
                                          ('leisure', 'Leisure'),
                                          ('interiors design', 'Interiors design'),
                                          ('construction', 'Construction'),
                                          ('trading', 'Trading'),
                                          ('others', 'Others')], string='Customer Type')
    x_mk_businessfacilities = fields.Char(string='Business Facilities')
    x_mk_clientgrade = fields.Selection([('A级', 'A级'),
                                         ('B级', 'B级'),
                                         ('C级', 'C级'),
                                         ('D级', 'D级')], string='Client Grade')
    x_mk_decisionaffected = fields.Char(string='Decision affected')
    x_mk_decisionhierarchy = fields.Selection([('高', 'High'),
                                               ('中', 'Medium'),
                                               ('低', 'Low')], string='Decision Hierarchy')
    x_mk_decisionlevel = fields.Selection([('高', 'High'),
                                           ('中', 'Medium'),
                                           ('低', 'Low')], string='Decision Level')
    x_mk_decisionmakingpower = fields.Selection([('是', '是'),
                                                 ('否', '否')], string='Decision Power')
    x_mk_existingmaterialusage = fields.Text(string='Material Usage')
    x_mk_existingprocurementchannels = fields.Selection([('本国品牌分销商', '本国品牌分销商'),
                                                         ('本国专业市场', '本国专业市场'),
                                                         ('本国进口贸易公司', '本国进口贸易公司'),
                                                         ('本国行业电商', '本国行业电商'),
                                                         ('自行从国外进口', '自行从国外进口')], string='Procurement Channels')
    x_mk_phase = fields.Selection([('规划', '规划'),
                                   ('设计', '设计'),
                                   ('建造', '建造'),
                                   ('开业筹备', '开业筹备'),
                                   ('酒店运营', '酒店运营')], string='Project Phase')
    x_mk_poolandwellness = fields.Text(string='Pool and Wellness')
    x_mk_recreationalfacilitiesandfamilyservices = fields.Text(string='Family Services Description')
    x_mk_pricepreference = fields.Selection([('低', '低'),
                                             ('中', '中'),
                                             ('高', '高'),
                                             ('极高', '极高')], string='Price Preference')
    x_mk_procurementurgency = fields.Text(string='Procurement Urgency')
    x_mk_productpreference = fields.Text(string='Product Preference')
    x_mk_purchaseingtime = fields.Selection([('第一季度', '第一季度'),
                                             ('第二季度', '第二季度'),
                                             ('第三季度', '第三季度'),
                                             ('第四季度', '第四季度')], string='Purchase Time')
    x_mk_rating = fields.Char(string='Rating')

    def view_phone(self):
        context = {
            'default_partner_id': self.id,
            'default_contract_type': 1,

        }
        domain = [('partner_id', '=', self.partner_id.id), ('contract_type', '=', 1)]
        view_id = self.env.ref('partner_advanced_design.res_partner_contract_tree')
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'tree,form',
                'res_model': 'res.partner',
                'target': 'current',
                'domain': domain,
                'context': context,
                'view_id': view_id.id,
                }

    def view_email(self):
        context = {
            'default_partner_id': self.id,
            'default_contract_type': 2,

        }
        domain = [('partner_id', '=', self.partner_id.id), ('contract_type', '=', 2)]
        view_id = self.env.ref('partner_advanced_design.res_partner_contract_tree')
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'tree,form',
                'res_model': 'res.partner',
                'target': 'current',
                'domain': domain,
                'context': context,
                'view_id': view_id.id,
                }


class PartnerCityRating(models.Model):
    _inherit = 'res.partner.category'

    supplier = fields.Boolean(string='Supplier')
    customer = fields.Boolean(string='Customer')

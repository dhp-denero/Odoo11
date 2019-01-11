# -*- coding: utf-8  -*-
import os
from datetime import datetime, timedelta

import lxml.etree as etree

from odoo.tools import config


def delegate_to_xml(delegation_list):
    '''根据委托清单对象生成完整的报文'''

    root = etree.Element("Root")
    head = etree.SubElement(root, "Head")
    body_list = etree.SubElement(root, "BodyList")

    head_node_dic = {
        'SyncNo': delegation_list.contract_num,
        'CreateDate': (datetime.now()+timedelta(hours=8)).strftime('%Y/%m/%d %H:%M:%S'),
        'QDType': '0',
        'IsEnabled': '1',
        'IsSendAgent': '0',
        'InventorySource': '1',
        'InventorySourceCN': '清单协同',
        'CreateUserID': '0',
        'CreateUserName': '清单协同',
        'BusinessCompanyId': '1111980068',
        'BusinessCompany': '北京运通安达报关有限公司',
        'InputCompanyId': '1111980068',
        'InputCompany': '北京运通安达报关有限公司',
        'TradeModeID': None,    #.text = delegation_list.trade_mode.code
        'TradeModeName': delegation_list.trade_mode.name,
        'GrossWeight': str(delegation_list.gross_weight),
        'NetWeight': str(delegation_list.net_weight),
        'Qty': str(delegation_list.num),
        'CustomerRefNO1': None,
        'CustomerRefNO2': None,
        'CustomerRefNO3': None,
        'Remark': None,
        'MBLNO': None,
        'SBLNO': None,
        'InOutName': '进口' if delegation_list.import_and_export == 'i' else '出口',
        'InOutID': delegation_list.import_and_export,
        'PartOrProduct': None,
        'PartOrProductName': None,
        'PortCN': delegation_list.customs.name,
        'PortCO': None,     #.text = delegation_list.customs.code
        'BuyerCompany': None,
        'BuyerCompanyId': None,
        'SellerCompany': None,
        'SellerCompanyId': None,
        'DeclareCompany': '北京运通安达报关有限公司',
        'DeclareCompanyId': '1111980068',
        'ContractNo': delegation_list.contract_num,
        'CustomerInnerCode': None,
        'LicenceNO': None,
        'Conveyance': None,
        'DealTypeCN': delegation_list.trade_term.name,
        'DealTypeID': None,
        'DutyCN': None,
        'DutyCO': None,
        'TransportTypeCN': None,
        'TransportTypeID': None,
        'PackageTypeCN': None,
        'PackageTypeID': None,
        'NationCN': delegation_list.origin_arrival_country.name,
        'NationCO': None,   #.text = delegation_list.origin_arrival_country.code
        'HavenCN': delegation_list.port.name,
        'HavenCO': None,    #.text = delegation_list.port.code
        'RegionCN': delegation_list.region.name,
        'RegionCO': None,   #.text = delegation_list.region.code
        'IsSH': '0',
        'IsSHType': None,
        'TradeCountryCN': delegation_list.trade_country.name,
        'TradeCountryCO': None,
        'InboundNumber': None,
        'NotifierId': None,
        'NotifierCN': None,
        'SendAgentType': '2',
        'SendAgentTypeName': '接单',
        'OrganizationCode': '201600022',
        'SystemType': 'CMS'
    }

    for node in head_node_dic:
        _node = etree.SubElement(head, node)
        value = head_node_dic[node]
        if value:
            _node.text = value


    # edit the bodylist
    for item in delegation_list.product_data_list:
        product_node_name = {
            'GoodsOrderID': str(delegation_list.id),
            'BillingNO': None,
            'DN': None,
            'PO': None,
            'CompanyBook': None,
            'CustomerBook': None,
            'CompanyItemNo': None,
            'CustomerItemNo': None,
            'CustomerPartNo': None,
            'HSCode_TS': item.hs_code.name,
            'HSCode_T': item.hs_code.name[0:7],
            'HSCode_S': item.hs_code.name[-2:],
            'CN_Name': item.chinese_name,
            'En_Name': item.english_name,
            'Model': None,
            'DealQty': str(item.qty_invoiced),
            'DealUnit': item.unit.name,
            'DealUnitID': None,  # .text = item.unit.code
            'GrossWeight': None,
            'NetWeight': None,
            'Volumn': None,
            'DealUnitPrice': str(item.price_unit),
            'DealAmount': str(item.price_subtotal),
            'CurrencyID': None,  # .text = item.currency.code
            'Currency': item.currency.name,
            'F_Qty': None,
            'F_UnitID': None,
            'F_Unit': None,
            'S_Qty': None,
            'S_UnitID': None,
            'S_Unit': None,
            'OriginCountry': item.delegate_country.name,
            'OriginCountryID': None,  # .text = item.delegate_country.code
            'DutyCO': None,
            'Duty': None,
            'PurposeCO': None,
            'Purpose': None,
            'Remark': None,
            'WarehouseSerialNo': None,
            'SupervisionIdentity': None,
            'CustomsId': None,
            'CustomsNo': None,
            'CompanyId': None,
            'CompanyName': None,
            'GoodsNo': None,
            'Supervision': None,
            'SupervisionStateId': None,
            'SupervisionState': None,
            'StateId': None,
            'GoodsState': None,
            'OrignalPlaceId': None,
            'OrignalPlace': None,
            'CusOrder': None,
            'CusQty1': None,
            'CusQty2': None,
            'CargoNO': None,
            'NationCO': None,
            'NationCN': None,
            'NationEN': None,
            'Manufacturer': None,
            'EntryID': None,
            'EntryIndx': None,
            'CargoIndx': None,
            'QDType': '0',
            'Old_InventoryId': None,
            'IsEnabled': 'True',
            'LineNumber': None,
            'IsRefilled': 'False',
            'WarehouseMode': None,
            'PartOrProduct': None,
            'CustomerBookOld': None,
            'CustomerItemNoOld': None,
            'InfoSerialNo': None,
            'DeclID': None,
            'DeclIndx': None,
            'DeclCargoIndx': None,
            'VersionNO': None,
            'Ref1': None,
            'Ref2': None,
            'Ref3': None,
            'containerType': None,
            'containerTypeName': None,
            'PalletsNum': None,
            'PalletsNumGrossWeight': None,
            'PalletsTypeEN': None
        }
        body = etree.SubElement(body_list, "Body")
        for node in product_node_name:
            _node = etree.SubElement(body, node)
            value = product_node_name[node]
            if value:
                _node.text = value


    # change the root to xml file
    string = etree.tostring(root, xml_declaration=True, encoding='utf-8')
    base_dir = config.options['xml_files_path']
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    obj_dir = os.path.join(base_dir, delegation_list.contract_num + '.xml')
    with open(obj_dir, 'w') as fp:
        fp.write(string.encode('utf8'))

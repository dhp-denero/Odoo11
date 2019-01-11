# -*- coding: utf-8  -*-
import json, requests, base64
from collections import OrderedDict


def delegation_to_json(delegation_list):
    '''利用交换平台的接口传输json格式的报文'''
    T_DHL_Inventory = OrderedDict()
    T_DHL_Inventory['CustomerInnerCode'] = delegation_list.contract_num
    T_DHL_Inventory['Remittance'] = None
    T_DHL_Inventory['InOutID'] = delegation_list.import_and_export
    T_DHL_Inventory['PortCO'] = delegation_list.customs.Code
    T_DHL_Inventory['PortCN'] = delegation_list.customs.NameCN
    T_DHL_Inventory['CurrencyID'] = '142'
    T_DHL_Inventory['Currency'] = u'人民币'
    T_DHL_Inventory['DealTypeID'] = delegation_list.trade_term.Code
    T_DHL_Inventory['DealTypeCN'] = delegation_list.trade_term.NameCN
    T_DHL_Inventory['TransportTypeID'] = delegation_list.transport.Code
    T_DHL_Inventory['TransportTypeCN'] = delegation_list.transport.NameCN
    T_DHL_Inventory['Qty'] = delegation_list.num
    T_DHL_Inventory['PackageTypeID'] = delegation_list.packing.Code
    T_DHL_Inventory['PackageTypeCN'] = delegation_list.packing.NameCN
    T_DHL_Inventory['WMTpye'] = '1'
    T_DHL_Inventory['NationCO'] = delegation_list.origin_arrival_country.Code
    T_DHL_Inventory['NationCN'] = delegation_list.origin_arrival_country.NameCN
    T_DHL_Inventory['TradeCountryCO'] = delegation_list.trade_country.Code
    T_DHL_Inventory['TradeCountryCN'] = delegation_list.trade_country.NameCN
    T_DHL_Inventory['ContractNo'] = delegation_list.contract_num
    T_DHL_Inventory['Remark'] = delegation_list.mark_code
    T_DHL_Inventory['DeclareCompanyId'] = '1111980068'
    T_DHL_Inventory['DeclareCompany'] = u'北京运通安达报关有限公司'
    T_DHL_Inventory['MerchantCompanyTel'] = None
    T_DHL_Inventory['MerchantCompanyMail'] = None
    T_DHL_Inventory['MerchantCompanyCustomCode'] = None
    T_DHL_Inventory['MerchantCompanySeal'] = None
    T_DHL_Inventory['MerchantCompanyLegalSeal'] = None
    T_DHL_Inventory['BusinessCompanyId'] = '1111980068'
    T_DHL_Inventory['BusinessCompany'] = u"北京运通安达报关有限公司"
    T_DHL_Inventory['MerchantCompanyTel'] = None
    T_DHL_Inventory['MerchantCompanyMail'] = None
    T_DHL_Inventory['BusinessCompanyId'] = '1111980068'
    T_DHL_Inventory['BusinessCompany'] = u'北京运通安达报关有限公司'
    T_DHL_Inventory['BusinessCompanyAddress'] = None
    T_DHL_Inventory['BusinessCompanyTel'] = None
    T_DHL_Inventory['BusinessCompanyMail'] = None

    T_DHL_Inventory_Goods_list = []

    for item in delegation_list.product_data_list:
        T_DHL_Inventory_Goods = OrderedDict()
        T_DHL_Inventory_Goods['CustomerInnerCode'] = 'NO1000'
        T_DHL_Inventory_Goods['CustomerPartNo'] = 'T002'
        T_DHL_Inventory_Goods['MaxPackingQty'] = None
        T_DHL_Inventory_Goods['NetWeight'] = '20'
        T_DHL_Inventory_Goods['GrossWeight'] = '20'
        T_DHL_Inventory_Goods['DealQty'] = item.qty_invoiced
        T_DHL_Inventory_Goods['DealUnitID'] = item.unit.Code
        T_DHL_Inventory_Goods['DealUnit'] = item.unit.NameCN
        T_DHL_Inventory_Goods['DealUnitPrice'] = item.price_unit
        T_DHL_Inventory_Goods['DealAmount'] = item.price_subtotal
        T_DHL_Inventory_Goods['CN_Name'] = item.chinese_name
        T_DHL_Inventory_Goods['HSCode_TS'] = item.hs_code.Code_TS
        T_DHL_Inventory_Goods['Model'] = u"用途|材质|其他"
        T_DHL_Inventory_Goods['PalletsNum'] = None
        # T_DHL_Inventory_Goods = {
        #     "CustomerInnerCode": 'NO1000',
        #     "CustomerPartNo": 'T002',
        #     "MaxPackingQty": None,
        #     "NetWeight": '20',
        #     "GrossWeight": '20',
        #     "DealQty": item.qty_invoiced,
        #     "DealUnitID": item.unit.code,
        #     "DealUnit": item.unit.name,
        #     "DealUnitPrice": item.price_unit,
        #     "DealAmount": item.price_subtotal,
        #     "CN_Name": item.chinese_name,
        #     "HSCode_TS": item.hs_code.name,
        #     "Model": u"用途|材质|其他",
        #     "PalletsNum": None
        # }
        T_DHL_Inventory_Goods_list.append(T_DHL_Inventory_Goods)

    T_DHL_Inventory["T_DHL_Inventory_Goods"] = T_DHL_Inventory_Goods_list
    T_DHL_Inventory['Attachment'] = None
    T_DHL_Inventory['TradeModeID'] = delegation_list.trade_mode.Code
    T_DHL_Inventory['TradeModeName'] = delegation_list.trade_mode.NameCN
    T_DHL_Inventory['RegionCO'] = delegation_list.region.Code
    T_DHL_Inventory['RegionCN'] = delegation_list.region.NameCN

    '''
                {
                    "CustomerInnerCode": delegation_list.contract_num,
                    "Remittance": None,
                    "InOutID": delegation_list.import_and_export,
                    "PortCO": delegation_list.customs.code,
                    "PortCN": delegation_list.customs.name,
                    "CurrencyID": '142',  # 币制存在表头还是产品里，需确认
                    "Currency": u'人民币',
                    "DealTypeID": delegation_list.trade_term.code,
                    "DealTypeCN": delegation_list.trade_term.name,
                    "TransportTypeID": delegation_list.transport.code,
                    "TransportTypeCN": delegation_list.transport.name,
                    "Qty": delegation_list.num,
                    "PackageTypeID": delegation_list.packing.code,
                    "PackageTypeCN": delegation_list.packing.name,
                    "WMTpye": "1",  # 整混包装方式是否需要添加到委托清单中需确认
                    "NationCO": delegation_list.origin_arrival_country.code,
                    "NationCN": delegation_list.origin_arrival_country.name,
                    "TradeCountryCO": delegation_list.trade_country.code,
                    "TradeCountryCN": delegation_list.trade_country.name,
                    "ContractNo": delegation_list.contract_num,
                    "Remark": delegation_list.mark_code,
                    "DeclareCompanyId": '1111980068',  # 申报单位在原有的xml格式和数据库中没有
                    "DeclareCompany": u'北京运通安达报关有限公司',
                    "MerchantCompanyTel": None,
                    "MerchantCompanyMail": None,
                    "MerchantCompanyCustomCode": None,
                    "MerchantCompanySeal": None,
                    "MerchantCompanyLegalSeal": None,
                    "BusinessCompanyId": "1111980068",  # 收货人编码没有
                    "BusinessCompany": u"北京运通安达报关有限公司",
                    "BusinessCompanyAddress": None,
                    "BusinessCompanyTel": None,
                    "BusinessCompanyMail": None,
                    "InputCompanyId": "1111980068",
                    "InputCompany": u'北京运通安达报关有限公司',
                    "InputCompanyAddress": None,
                    "InputCompanyTel": None,
                    "InputCompanyMail": None,
                    "T_DHL_Inventory_Goods": None,
                    "Attachment": None,
                    "TradeModeID": delegation_list.trade_mode.code,
                    "TradeModeName": delegation_list.trade_mode.name,
                    "RegionCO": delegation_list.region.code,
                    "RegionCN": delegation_list.region.name
                }
                '''
    dic = {
        "T_DHL_Inventory": [
            T_DHL_Inventory
        ]
    }

    demo = {
        "T_DHL_Inventory":[
            {
                "CustomerInnerCode": "NO1000",
                "Remittance": "0-T/T",
                "InOutID": 'e',
                "PortCO": "0100",
                "PortCN": "北京关区",
                "CurrencyID": "142",
                "Currency": "人民币",
                "DealTypeID": "3",
                "DealTypeCN": "FOB",
                "TransportTypeID": "2",
                "TransportTypeCN": "水路运输",
                "Qty": "100",
                "PackageTypeID": "1",
                "PackageTypeCN": "木箱",
                "WMTpye": "1",
                "NationCO": "142",
                "NationCN": "中国",
                "TradeModeID ": "0110 ",
                "TradeModeName": "一般贸易",
                "HavenCO": " ",
                "HavenCN": " ",
                "RegionCO": "11019",
                "RegionCN": "东城区",
                "TradeCountryCO": "502",
                "TradeCountryCN": "美国",
                "ContractNo": "TEST001",
                "Remark": "111",
                "DeclareCompanyId": "1111980068",
                "DeclareCompany": "北京运通安达报关有限公司",
                "MerchantCompanyId": "001 ",
                "MerchantCompany": "测试商户",
                "MerchantOrganizationCode": "001",
                "MerchantCompanyTel": "XXXXXXXXXXX",
                "MerchantCompanyMail": "XXX@163.com",
                "MerchantCompanyCustomCode": "XXXXXXXXXX",
                "MerchantCompanySeal": "XXX",
                "MerchantCompanyLegalSeal": "XXX",
                "BusinessCompanyId": "3456754321",
                "BusinessCompany": "中国丝绸服装进出口公司",
                "BusinessCompanyAddress": "XXXXX路XXX号",
                "BusinessCompanyTel": "XXXXXXXXXX",
                "BusinessCompanyMail": "XXX@163.com",
                "InputCompanyId": "3456754321",
                "InputCompanyOrganizationCode": "001 ",
                "InputCompany": "中国丝绸服装进出口公司",
                "InputCompanyAddress": "XXXXX路XXX号",
                "InputCompanyTel": "XXXXXXXXXXX",
                "InputCompanyMail": "XXX@163.com",
                "T_DHL_Inventory_Goods": [
                    {
                        "CustomerPartNo": "T001",
                        "MaxPackingQty": "10",
                        "NetWeight": "10",
                        "GrossWeight": "10",
                        "DealQty": "10",
                        "DealUnitID": "001",
                        "DealUnit": "台",
                        "DealUnitPrice": "10",
                        "DealAmount": "100",
                        "CN_Name": "用植物性材料制作的人体模型",
                        "HSCode_TS": "9618000010",
                        "Model": "用途|材质|其他",
                        "PalletsNum": "ZZZ0001"
                    },
                    {
                        "CustomerPartNo": "T002",
                        "MaxPackingQty": "20",
                        "NetWeight": "20",
                        "GrossWeight": "20",
                        "DealQty": "20",
                        "DealUnitID": "001",
                        "DealUnit": "台",
                        "DealUnitPrice": "20",
                        "DealAmount": "400",
                        "CN_Name": "烟气脱硝装置",
                        "HSCode_TS": "8421395000",
                        "Model": "用途|原理|品牌|型号|额定功率（非电动的不需注明额定功率）|其他",
                        "PalletsNum": "ZZZ0001"
                    }
                ],
                "Attachment": [
                    {
                        "URL": " abc.com123elsx",
                        "FileType": "Packing"
                    },
                    {
                        "URL": " abc.com123elsx",
                        "FileType": "Invoice"
                    }
                ]
            }
        ]
    }



    data = json.dumps(dic, encoding='utf-8')
    print(data)
    data = base64.b64encode(data)
    print(data)


    reponse = requests.post('http://47.93.158.94:8000/T_DHL_Inventory_Unified', data=data)
    # data = base64.b64decode(data)
    # data = json.loads(data)
    # print(data['T_DHL_Inventory'][0]['DeclareCompany'])
    # print(type(data['T_DHL_Inventory'][0]['DeclareCompany']))

    print(reponse.text)


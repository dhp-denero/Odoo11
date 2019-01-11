# -*- coding: utf-8 -*-
import werkzeug
import json
import base64
from random import randint
import os
import datetime
import requests
import logging
_logger = logging.getLogger(__name__)

import openerp.http as http
from openerp.http import request
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.http_routing.models.ir_http import slug


class SaleRequirementController(http.Controller):
    @http.route('/bussiness/requirement', type="http", auth="public", website=True)
    def business_requirement(self, **kw):
        """Displays all help groups and thier child help pages"""

        return http.request.render('website_requirement.sale_requirement_pages', {})

    @http.route('/business/requirement/view', type="http", auth="user", website=True)
    def sale_requirement_view_list(self, **kw):
        """Displays a list of support tickets owned by the logged in user"""

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value




        sale_requirement = request.env['sale.requirement'].sudo().search([])
        # 
        requirement_scenario = request.env['scenario.tags'].sudo().search([])


        return request.render('website_requirement.sale_requirement_view_list', {'sale_requirement':sale_requirement,'requirement_count':len(sale_requirement), 'requirement_scenario': requirement_scenario})

    @http.route('/business/requirement/view/<requirement>', type="http", auth="user", website=True)
    def support_ticket_view(self, requirement):
        """View an individual support ticket"""

        #only let the user this ticket is assigned to view this ticket
        sale_requirement = http.request.env['sale.requirement'].sudo().search([('id','=',requirement)])[0]
        return http.request.render('website_requirement.sale_requirement_view', {'sale_requirement':sale_requirement})

    @http.route('/business/requirement/submit', type="http", auth="public", website=True)
    def business_submit_requirement(self, **kw):
        """Let's public and registered user submit a support ticket"""
        category_access = []
        for category_permission in http.request.env.user.groups_id:
            category_access.append(category_permission.id)
        
        requirement_scenario = request.env['scenario.tags'].sudo().search([])

        setting_google_recaptcha_active = request.env['ir.default'].get('website.requirement.settings', 'google_recaptcha_active')
        setting_google_captcha_client_key = request.env['ir.default'].get('website.requirement.settings', 'google_captcha_client_key')
        setting_max_ticket_attachments = request.env['ir.default'].get('website.requirement.settings', 'max_ticket_attachments')
        setting_max_ticket_attachment_filesize = request.env['ir.default'].get('website.requirement.settings', 'max_ticket_attachment_filesize')
        setting_allow_website_priority_set = request.env['ir.default'].get('website.requirement.settings', 'allow_website_priority_set')
        
        return http.request.render('website_requirement.business_submit_requirement', {'requirement_scenario': requirement_scenario, 'staff_id': http.request.env.user.partner_id, 'setting_max_ticket_attachments': setting_max_ticket_attachments, 'setting_max_ticket_attachment_filesize': setting_max_ticket_attachment_filesize, 'setting_google_recaptcha_active': setting_google_recaptcha_active, 'setting_google_captcha_client_key': setting_google_captcha_client_key, })

    @http.route('/business/requirement/process', type="http", auth="public", website=True, csrf=True)
    def support_process_ticket(self, **kwargs):
        """Adds the support ticket to the database and sends out emails to everyone following the support ticket category"""
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        if values['my_gold'] != "256":
            return "Bot Detected"

        setting_google_recaptcha_active = request.env['ir.default'].get('website.requirement.settings', 'google_recaptcha_active')
            
        if setting_google_recaptcha_active:

            setting_google_captcha_secret_key = request.env['ir.default'].get('website.requirement.settings', 'google_captcha_secret_key')

            #Redirect them back if they didn't answer the captcha
            if 'g-recaptcha-response' not in values:
                return werkzeug.utils.redirect("/business/requirement/submit")

            payload = {'secret': setting_google_captcha_secret_key, 'response': str(values['g-recaptcha-response'])}
            response_json = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)

            if response_json.json()['success'] is not True:
                return werkzeug.utils.redirect("/business/requirement/submit")
                
        my_attachment = ""
        file_name = ""
        name = ""


        create_dict = {'name':values['name'],'description':values['description'], 'attachment': my_attachment, 'attachment_filename': file_name}

        if http.request.env.user.name != "Public user":

            create_dict['channel'] = 'Website (User)'
            
            partner = http.request.env.user.partner_id
            create_dict['staff_id'] = partner.id


            #Add to the communication history of the logged in user
            partner.message_post(body="Customer " + partner.name + " has create a new Project")
        else:

            create_dict['channel'] = 'Website (Public)'
            
            #Automatically assign the partner if email matches
            search_partner = request.env['res.partner'].sudo().search([('email','=', values['email'] )])
            if len(search_partner) > 0:
                create_dict['partner_id'] = search_partner[0].id

        new_requirement_id = request.env['sale.requirement'].sudo().create(create_dict)

        if 'file' in values:

            for c_file in request.httprequest.files.getlist('file'):
                data = c_file.read()

                if c_file.filename:
                    request.env['ir.attachment'].sudo().create({
                        'name': c_file.filename,
                        'datas': base64.b64encode(data),
                        'datas_fname': c_file.filename,
                        'res_model': 'sale.requirement',
                        'res_id': new_requirement_id.id
                    })

        return werkzeug.utils.redirect("/business/requirement/thanks")

    @http.route('/business/requirement/thanks', type="http", auth="public", website=True)
    def sale_requirement_thanks(self, **kw):
        """Displays a thank you page after the user submits a ticket"""
        return http.request.render('website_requirement.support_thank_you', {})


class ProductQuotationController(http.Controller):

    def _get_search_domain(self, search):
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|',  ('name', 'ilike', srch), ('department', 'ilike', srch),
                    ('application', 'ilike', srch)]

        return domain

    @http.route('/business/<requirement>/quotation', type='http', auth="user", website=True)
    def product_quotation_view_list(self, requirement,search=''):
        
        domain = self._get_search_domain(search)
        
        domain += [('requirement_id','=',int(requirement))]

        product_quotation = http.request.env['product.quotation'].search(domain)


        return request.render('website_requirement.product_quotation_view_list', {'product_quotation':product_quotation,'quotation_count':len(product_quotation)})

    @http.route('/business/quotation/<quotation>/views', type="http", auth="user", website=True)
    def support_ticket_view(self, quotation):
        """View an individual support ticket"""

        #only let the user this ticket is assigned to view this ticket
        product_quotation = http.request.env['product.quotation'].sudo().search([('id','=',quotation)])[0]
        return http.request.render('website_requirement.product_quotation_view', {'product_quotation':product_quotation})


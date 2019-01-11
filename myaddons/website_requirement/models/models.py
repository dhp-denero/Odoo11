# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
import requests
from openerp.http import request
import odoo

from openerp import api, fields, models

class WebsiteSupportSettings(models.Model):

    _name = "website.requirement.settings"
    _inherit = 'res.config.settings'

    close_ticket_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket')]", string="(OBSOLETE)Close Ticket Email Template")
    change_user_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket')]", string="Change User Email Template")
    staff_reply_email_template_id = fields.Many2one('mail.template', domain="[('model_id','=','website.support.ticket.compose')]", string="Staff Reply Email Template")
    email_default_category_id = fields.Many2one('website.support.ticket.categories', string="Email Default Category")
    max_ticket_attachments = fields.Integer(string="Max Ticket Attachments")
    max_ticket_attachment_filesize = fields.Integer(string="Max Ticket Attachment Filesize (KB)")
    allow_user_signup = fields.Boolean(string="Allow User Signup")
    auto_send_survey = fields.Boolean(string="Auto Send Survey")
    business_hours_id = fields.Many2one('resource.calendar', string="Business Hours")
    google_recaptcha_active = fields.Boolean(string="Google reCAPTCHA Active")
    google_captcha_client_key = fields.Char(string="reCAPTCHA Client Key")
    google_captcha_secret_key = fields.Char(string="reCAPTCHA Secret Key")

    @api.multi
    def set_values(self):
        super(WebsiteSupportSettings, self).set_values()
        self.env['ir.default'].set('website.requirement.settings', 'auto_send_survey', self.auto_send_survey)
        self.env['ir.default'].set('website.requirement.settings', 'allow_user_signup', self.allow_user_signup)
        self.env['ir.default'].set('website.requirement.settings', 'change_user_email_template_id', self.change_user_email_template_id.id)
        self.env['ir.default'].set('website.requirement.settings', 'close_ticket_email_template_id', self.close_ticket_email_template_id.id)
        self.env['ir.default'].set('website.requirement.settings', 'email_default_category_id', self.email_default_category_id.id)
        self.env['ir.default'].set('website.requirement.settings', 'staff_reply_email_template_id', self.staff_reply_email_template_id.id)
        self.env['ir.default'].set('website.requirement.settings', 'max_ticket_attachments', self.max_ticket_attachments)
        self.env['ir.default'].set('website.requirement.settings', 'max_ticket_attachment_filesize', self.max_ticket_attachment_filesize)
        self.env['ir.default'].set('website.requirement.settings', 'business_hours_id', self.business_hours_id.id)
        self.env['ir.default'].set('website.requirement.settings', 'google_recaptcha_active', self.google_recaptcha_active)
        self.env['ir.default'].set('website.requirement.settings', 'google_captcha_client_key', self.google_captcha_client_key)
        self.env['ir.default'].set('website.requirement.settings', 'google_captcha_secret_key', self.google_captcha_secret_key)
        
    @api.model
    def get_values(self):
        res = super(WebsiteSupportSettings, self).get_values()
        res.update(
            auto_send_survey=self.env['ir.default'].get('website.requirement.settings', 'auto_send_survey'),
            allow_user_signup=self.env['ir.default'].get('website.requirement.settings', 'allow_user_signup'),
            change_user_email_template_id=self.env['ir.default'].get('website.requirement.settings', 'change_user_email_template_id'),
            close_ticket_email_template_id=self.env['ir.default'].get('website.requirement.settings', 'close_ticket_email_template_id'),
            email_default_category_id=self.env['ir.default'].get('website.requirement.settings', 'email_default_category_id'),
            staff_reply_email_template_id=self.env['ir.default'].get('website.requirement.settings', 'staff_reply_email_template_id'),
            max_ticket_attachments=self.env['ir.default'].get('website.requirement.settings', 'max_ticket_attachments'),
            max_ticket_attachment_filesize=self.env['ir.default'].get('website.requirement.settings', 'max_ticket_attachment_filesize'),
            business_hours_id=self.env['ir.default'].get('website.requirement.settings', 'business_hours_id'),
        )
        return res

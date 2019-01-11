# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    contacts_count = fields.Integer(string='Contact counts', compute='_number_of_contacts')
    leave_date = fields.Date(string='Leave Date')

    # 计算联系方式数量
    @api.depends()
    def _number_of_contacts(self):
        for s in self:
            domain = [('applicant_id', '=', s.id)]
            count = len(s.env['res.contacts'].search(domain).ids)
            s.contacts_count = count

    @api.multi
    def action_res_contacts(self):
        context = {
            'default_applicant_id_id': self.id,
        }
        domain = [('applicant_id', '=', self.id)]
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'tree',
                'res_model': 'res.contacts',
                'target': 'new',
                'context': context,
                'domain': domain,
                }


class ResContracts(models.Model):
    _name = 'res.contacts'
    _description = 'Contacts Management'

    type = fields.Selection([('1', 'website'), ('2', 'Online'), ('3', 'Offline'), ('4', 'Others')], string='Type')
    name = fields.Char(string='Description')
    applicant_id = fields.Many2one('hr.applicant', string='Applicant')

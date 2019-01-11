# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import datetime

class HrMissing(models.Model):
    _name = 'hr.missing'

    name = fields.Char('Name')
    description = fields.Text('Description')
    grade = fields.Selection(
        [('green', 'A RANK'),
         ('black', 'B RANK'),
         ('red', 'C RANK')],
        string='Missing Grade',
        default='green')
    score = fields.Float('Score')
    percentage = fields.Float('Per.')


class HrMissingLine(models.Model):
    _name = 'hr.missing.line'

    missing_id = fields.Many2one('hr.missing', string='Missing')
    employee_id = fields.Many2one('hr.employee', string='Empolyee')
    user_id = fields.Many2one('res.users', related='employee_id.user_id')
    coach_id = fields.Many2one('hr.employee', related='employee_id.coach_id')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id')
    name = fields.Text('Description')
    date = fields.Date(string='Date', default=fields.Date.today(),store=True)
    month = fields.Integer(string='Month', compute='_compute_year_month',store=True)
    year = fields.Integer(string='Year', compute='_compute_year_month',store=True)

    @api.depends('date')
    @api.onchange('date')
    def _compute_year_month(self):
        for s in self:
            s.month = datetime.datetime.strptime(s.date, '%Y-%m-%d').strftime('%m')
            s.year = datetime.datetime.strptime(s.date, '%Y-%m-%d').strftime('%Y')

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    missing_count = fields.Integer(string='Missing', compute='_number_of_missing')

    @api.depends()
    def _number_of_missing(self):
        for s in self:
            domain = [('employee_id', '=', s.id),
                      ('month', '=', datetime.date.today().strftime('%m')),
                      ('year', '=', datetime.date.today().strftime('%Y')), ]
            count = len(s.env['hr.missing.line'].search(domain).ids)
            s.missing_count = count

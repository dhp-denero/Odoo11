# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo import exceptions
import datetime
from datetime import datetime
import calendar


class TimesheetLine(models.Model):
    _inherit = 'account.analytic.line'

    month = fields.Integer(string='Month', compute='_compute_year_month', store=True)
    year = fields.Integer(string='Year', compute='_compute_year_month', store=True)
    x_task_worked = fields.Float(string='Worked Time(Hour)')
    x_task_quality = fields.Float(string='Work Quality')
    x_task_effetive = fields.Float(string='Work Effetive', compute='_compute_effetive')
    is_finished_task = fields.Boolean(string='Finished',default=False)

    @api.one
    def _compute_effetive(self):
        for r in self:
            if r.x_task_worked:
                r.x_task_effetive = (r.unit_amount / r.x_task_worked)

    @api.depends('date')
    @api.onchange('date')
    def _compute_year_month(self):
        for s in self:
            s.month = datetime.strptime(s.date, '%Y-%m-%d').strftime('%m')
            s.year = datetime.strptime(s.date, '%Y-%m-%d').strftime('%Y')

    @api.multi
    def button_activity(self):
        if self.is_finished_task:
            raise exceptions.Warning('This timesheet has been balanced.')
        else:
            time = datetime.now()
            date = datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S')
            hour = self.employee_id.resource_calendar_id.get_work_hours_count(start_dt=date, end_dt=time,
                                                                              compute_leaves=True,
                                                                              resource_id=self.env[
                                                                                  'resource.resource'].search(
                                                                                  [('user_id', '=',
                                                                                    self.employee_id.id)]).id)
            self.x_task_worked = hour
            activity_id = self.env['mail.activity.type'].search([('name', '=', 'Todo')])
            model_id = self.env['ir.model'].search([('model', '=', 'project.task')])
            date = fields.Date.today()
            note = '%s in %s had been finished by %s .Please check the completion of it.' % (self.name,self.task_id.name,self.employee_id.name)
            pdt_value = {
                'res_id': self.task_id.id,
                'res_model_id': model_id.id,
                'user_id': self.task_id.user_id.id,
                'date_deadline': date,
                'note': note,
                'activity_type_id': activity_id.id,
            }
            self.env['mail.activity'].create(pdt_value)


    @api.one
    def btn_todo(self):
        self.is_finished_task = not self.is_finished_task
        activity_id = self.env['mail.activity.type'].search([('name', '=', 'Todo')])
        model_id = self.env['ir.model'].search([('model', '=', 'project.task')])
        date = fields.Date.today()
        note = '%s in %s had not been finished . %s please check it out again.' % (
        self.name, self.task_id.name, self.employee_id.name)
        pdt_value = {
            'res_id': self.task_id.id,
            'res_model_id': model_id.id,
            'user_id': self.task_id.user_id.id,
            'date_deadline': date,
            'note': note,
            'activity_type_id': activity_id.id,
        }
        self.env['mail.activity'].create(pdt_value)
        self.is_finished_task = True
        return True

class HrPersonality(models.Model):
    _name = 'hr.employee.personality'

    rvalue = fields.Float(string='Responsibility')
    dvalue = fields.Float(string='Discipline')
    cvalue = fields.Float(string='Capacity')
    wvalue = fields.Float(string='Sense of worth')
    date = fields.Date(string='Date', default=fields.Date.today())
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one('res.users', string='Graders')
    score = fields.Float(string='Monthly Grade', compute='_score_monthly')
    month = fields.Integer(string='Month', compute='_compute_year_month', store=True)
    year = fields.Integer(string='Year', compute='_compute_year_month', store=True)

    @api.depends('date')
    @api.onchange('date')
    def _compute_year_month(self):
        for s in self:
            s.month = datetime.strptime(s.date, '%Y-%m-%d').strftime('%m')
            s.year = datetime.strptime(s.date, '%Y-%m-%d').strftime('%Y')

    @api.onchange('rvalue', 'dvalue', 'cvalue', 'wvalue')
    @api.depends('rvalue', 'dvalue', 'cvalue', 'wvalue')
    def _score_monthly(self):
        for s in self:
            domain = [('employee_id', '=', s.id),
                      ('month', '=', datetime.today().strftime('%m')),
                      ('year', '=', datetime.today().strftime('%Y')), ]
            number = len(self.search(domain).ids)
            person = self.search(domain)
            if number:
                if person.employee_id.parent_id.user_id.id == person.user_id.id:
                    self.score = ((person.rvalue + person.dvalue + person.cvalue + person.wvalue) * 4) / (7 * number)
                else:
                    self.score = (person.rvalue + person.dvalue + person.cvalue + person.wvalue) / (7 * number)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    timesheet_count = fields.Integer(string='Timesheet', compute='_number_of_timesheet')
    monthly_score = fields.Float(string='Monthly Score', compute='_compute_month_score')
    worked_time = fields.Float(string='Worked Time', compute='_compute_month_score')
    need_grade = fields.Boolean(string='Need Grade',compute='_need_grade')
    employee_grade = fields.One2many('hr.employee.personality', 'employee_id')
    work_quality = fields.Float(string='Capacity')

    @api.model
    def _need_grade(self):
        for emp in self:
            if emp.user_id:
                domain = [('employee_id', '=', emp.id),
                          ('month', '=', datetime.today().strftime('%m')),
                          ('year', '=', datetime.today().strftime('%Y')), ]
                count = len(emp.env['hr.employee.personality'].search(domain).ids)
                if count == 0:
                    emp.need_grade = True
                else:
                    emp.need_grade = False

    # @api.multi
    # def _create_grade_activity_(self):
    #     parent = []
    #     if self.coach_id:
    #         parent.append(self.coach_id.user_id.id)
    #     if self.parent_id:
    #         parent.append(self.parent_id.user_id.id)
    #     for user in parent:
    #         note = 'Please evaluate the performance of %s in this month.' % self.name
    #         activity_id = self.env['mail.activity.type'].search([('name', '=', 'Todo')])
    #         model_id = self.env['ir.model'].search([('model', '=', 'hr.employee')])
    #         date = fields.Date.today()
    #         pdt_value = {
    #             'res_id': self.id,
    #             'res_model_id': model_id.id,
    #             'user_id': user,
    #             'date_deadline': date,
    #             'note': note,
    #             'activity_type_id': activity_id.id,
    #         }
    #         self.env['mail.activity'].create(pdt_value)

    @api.one
    def _number_of_timesheet(self):
        for s in self:
            domain = [('employee_id', '=', s.id),
                      ('month', '=', datetime.today().strftime('%m')),
                      ('year', '=', datetime.today().strftime('%Y')), ]
            count = len(s.env['account.analytic.line'].search(domain).ids)
            self.worked_time += s.env['account.analytic.line'].search(domain).x_task_worked
            s.timesheet_count = count

    @api.onchange('timesheet_count')
    @api.one
    def _compute_month_score(self):
        if self.timesheet_count:
            for s in self:
                domain = [('employee_id', '=', s.id),
                          ('month', '=', datetime.today().strftime('%m')),
                          ('year', '=', datetime.today().strftime('%Y')), ]
                timesheet = s.env['account.analytic.line'].search(domain)
                person = s.env['hr.employee.personality'].search(domain)
                task_score = 0.0
                person_score = 0.0
                worked_time = 0.0
                task_quality = 0.0
                task_effetive = 0.0
                missing_score = 0.0
                # 工作得分
                for timesheet in timesheet:
                    task_quality += timesheet.x_task_quality
                    quality_score = (task_quality / self.timesheet_count) * 0.8 + self.work_quality * 0.2

                    task_effetive += timesheet.x_task_effetive
                    effetive_score = (task_effetive / self.timesheet_count) * 15

                    worked_time += timesheet.unit_amount
                    time = datetime.today()
                    timerange = calendar.monthrange(time.year, time.month)[-1]
                    amouth_score = (worked_time / self.resource_calendar_id.get_work_hours_count(
                        start_dt=datetime.today().replace(day=1),
                        end_dt=datetime.today().replace(day=int(timerange)),
                        resource_id=self.env['resource.resource'].search([('user_id', '=', s.user_id.id)]).id)) * 30

                    missing_score += self.env['hr.missing.line'].search(domain).missing_id.score

                    task_score = quality_score + effetive_score + amouth_score - missing_score
                # 个人得分
                for person in person:
                    person_score += person.score

                    self.monthly_score = task_score + person_score

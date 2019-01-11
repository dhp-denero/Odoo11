# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
from pytz import timezone,all_timezones
import logging
_logger = logging.getLogger(__name__)
try:
    from zk3 import ZK
except ImportError:
    raise ImportError('This module needs pyzk3 to fetch attendance from zk device in Odoo 11.')

class BiomtericDeviceInfo(models.Model):

    _name = 'biomteric.device.info'
    _inherit = ['mail.thread']

    @api.model
    def fetch_attendance(self):
        machines = self.search([])
        for machine in machines:
            if machine.apiversion == 'ZKLib':
                machine.download_attendance_oldapi()
            
    @api.multi
    def test_connection_device(self):
        zk = ZK(self.ipaddress, int(self.portnumber), timeout=90)
        res = zk.connect()
        if not res:
            raise ValidationError('Connection Failed to Device '+str(self.name))
        else:
            raise ValidationError('Connection Successful '+str(self.name))

    @api.one
    def get_local_utc(self, offset):
        hours = offset[1:3]
        minutes = offset[3:5]
        return [int(hours),int(minutes)]

    @api.one
    def download_attendance_oldapi(self):
        if self.fetch_days >= 0:
            now_datetime = datetime.datetime.now()
            prev_datetime = now_datetime - datetime.timedelta(days=self.fetch_days)
            curr_date = prev_datetime.date() 
        else:
            curr_date = '1950-01-01'
            
        zk = ZK(self.ipaddress, int(self.portnumber), timeout=90)
        res = zk.connect()
        attendance = res.get_attendance()
        if (attendance):
            hr_attendance =  self.env['hr.draft.attendance']
            for lattendance in attendance:
                #curr_date = '2017-10-31'
                if str(curr_date) <= str(lattendance.timestamp.date()):
                    my_local_timezone = timezone(self.time_zone)
                    local_date = my_local_timezone.localize(lattendance.timestamp)
                    utcOffset = local_date.strftime('%z')
                    hours , minutes = self.get_local_utc(utcOffset)[0]
                    time_att = str(lattendance.timestamp.date()) + ' ' +str(lattendance.timestamp.time())
                    atten_time1 = datetime.datetime.strptime(str(time_att), '%Y-%m-%d %H:%M:%S')
                    if utcOffset[0] == '+':
                        atten_time = atten_time1 - datetime.timedelta(hours=hours,minutes=minutes)
                    elif utcOffset[0] == '-':
                        atten_time = atten_time1 + datetime.timedelta(hours=hours,minutes=minutes)
                    else:
                        atten_time = atten_time1
                    atten_time = datetime.datetime.strftime(atten_time, '%Y-%m-%d %H:%M:%S')
                    att_id = lattendance.user_id
                    if att_id:
                        att_id = str(att_id)
                    else:
                        att_id = ''
                    employees = self.env['employee.attendance.devices'].search([('attendance_id', '=', att_id), ('device_id', '=', self.id)])
                    try:
                        atten_ids = hr_attendance.search([('employee_id','=',employees.name.id), ('name','=',atten_time)])
                        if atten_ids:
                            _logger.info('Attendance For Employee' + str(employees.name.name)+ 'on Same time Exist')
                            continue
                        else:
                            if self.action == 'both':
                                if not employees.name:
                                    continue
                                action = self.get_day_worktime(employees.name, lattendance.timestamp.strftime('%A'), lattendance.timestamp.date(), lattendance.timestamp)[0]
                            else:
                                action = self.action
                                
                            if lattendance.timestamp.strftime('%A') == 'Friday':
                                action = 'sign_none'
                                
                            if action != False:
                                if not employees.name.id:
                                    _logger.info('No Employee record found to be associated with User ID: ' + str(att_id)+ ' on Finger Print Mahcine')
                                    continue
                                atten_id = hr_attendance.create({'name':atten_time,
                                                                'employee_id':employees.name.id,
                                                                'date':lattendance.timestamp.date(),
                                                                'attendance_status': action,
                                                                'day_name': lattendance.timestamp.strftime('%A')})
                                _logger.info('Creating Draft Attendance Record: ' + str(atten_id) + 'For '+ str(employees.name.name))                                
                    except Exception as e:
                        print ('Exception', str(e))
                        pass
        return True

    @api.one
    def get_day_worktime(self, employee, day_id, date, atte_datetime):
        day_of_week = {'Monday':0 ,'Tuesday':1 ,'Wednesday':2 ,'Thursday':3 ,'Friday':4 ,'Saturday':5 ,'Sunday':6 }
        contract_id = self.env['hr.payslip'].get_contract(employee, date, date)
        action = 'sign_none'
        if contract_id:
            contract = self.env['hr.contract'].browse(contract_id)
            if contract.resource_calendar_id:
                for day in contract.resource_calendar_id.attendance_ids:
                    if int(day.dayofweek) == day_of_week[day_id]:
                        time_hour = day.hour_from
                        in_out_time = self.convert_to_float(str(atte_datetime.time()))[0]
                        in_diff  = in_out_time-time_hour
                        out_diff = day.hour_to-in_out_time
                        # 5,4 range (ex : from 8AM to 1PM sign_in , from 1PM to 5PM sign_out)
                        if in_diff <= 5:
                            action = 'sign_in'
                        elif out_diff <= 4:
                            action = 'sign_out'
                        return action
        else:
            return False
        
    name = fields.Char(string='Device', required=True)
    ipaddress = fields.Char(string='IP Address', required=True)
    portnumber = fields.Integer(string='Port', required=True)
    firmwareinfo = fields.Char(string='Firmware')
    fetch_days = fields.Integer('Automatic Fetching Period (days)', deafult=0)
    action = fields.Selection(selection=[('sign_in','Sign In'),('sign_out','Sign Out'),('both','All')], string='Action', default='sign_in', required=True)
    vendor = fields.Many2one(comodel_name='biomteric.device.vendor', string='Device', required=True)
    apiversion = fields.Selection(selection=[('ZKLib', 'ZKLib'), ('SOAPpy', 'SOAPpy')], string='API', default='ZKLib')
    time_zone = fields.Selection('_tz_get', string='Timezone', required=True, default=lambda self: self.env.user.tz or 'UTC')
    
    @api.model
    def _tz_get(self):
        return [(x, x) for x in all_timezones]
    
    @api.one
    @api.constrains('name')
    def _check_unique_constraint(self):
        record = self.search([('name', '=', self.name)])
        if len(record) > 1:
            raise ValidationError('Device ('+str(self.name)+') already exists and violates unique field constraint')

    @api.one
    def convert_to_float(self, time_att):
        h_m_s = time_att.split(":")
        hours = int(h_m_s[0])
        minutes_1 = float(h_m_s[1])/60.0
        minutes = ("%.2f" % minutes_1)
        return hours+float(minutes)

class BiomtericDeviceVendor(models.Model):

    _name = 'biomteric.device.vendor'

    name = fields.Char(string='Device', required=True)
    contact_number = fields.Char(string='Contact #')

    @api.one
    @api.constrains('name')
    def _check_unique_constraint(self):
        record = self.search([('name', '=', self.name)])
        if len(record) > 1:
            raise ValidationError('Vendor ('+str(self.name)+') already exists and violates unique field constraint')
    
    

# coding=utf-8
from pyzabbix import ZabbixAPI
import datetime
from datetime import date
import time
from time import sleep
import re
import extras.send_mail as mail_send
import modules.glpi_create_ticket as glpi_crt
import modules.zbx_tts_converter as zbx_conv
import modules.zbxtg.zbx_tg as zbx_teleg
import modules.zbx_set_ack as zbx_ack
import modules.create_message as msg_crt
import modules.asterisk_make_call as asterisk
import database
from configparser import ConfigParser


cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

timenow = datetime.datetime.now()
print(timenow, "- Control Manager: Starting zp_manager process...")

def zp_manager():
    def mysqlupdate():
        sql = "UPDATE zp_events SET TriggerChecked = %s WHERE TriggerZbxId = %s"
        val = ("Yes", event[0])
        database.mycursor.execute(sql, val)
    
    # Set variables to connection with Zabbix API
    ZbxServer = cfg.get('zabbix', 'zbx_api_url')
    ZbxUsername = cfg.get('zabbix', 'zbx_user')
    ZbxPassword = cfg.get('zabbix', 'zbx_pass')
    
    # Zabbix API Server
    zbxapi = ZabbixAPI(ZbxServer)
    
    # Zabbix API Authentication
    zbxapi.login(ZbxUsername, ZbxPassword)
    
    # Specify a timeout (in seconds)
    zbxapi.timeout = 5.1
    
    # Sql query to get issues to notification
    sql = "SELECT TriggerZbxId, TriggerZbxLastChange, TriggerZbxDesc, " \
          "TriggerZbxHost, TriggerTime FROM zp_events WHERE TriggerChecked = 'No'"
    database.mycursor.execute(sql)
    sqlresult = database.mycursor.fetchall()
    
    # current date and time
    timenow = datetime.datetime.now()

    # convert current date and time to timestamp
    timestampnow = datetime.datetime.timestamp(timenow)
    
    # Print zabbix connection
    print(timenow, "- Zabbix API: Connected to version %s" % zbxapi.api_version())
    print(timenow, "- Zabbix API: Checking zabbix issues ready to alert...")
    
    # Load parameters from worktime
    in_office = cfg.get('worktime', 'in_office_time')
    time_in = in_office.split("-")
    out_office = cfg.get('worktime', 'out_office_time')
    time_out = out_office.split("-")
    
    datetoday = date.today()
    dayweek = datetoday.weekday()
    
    dayworkin = cfg.get('workday', 'in_office_days')
    dayworkout = cfg.get('workday', 'out_office_days')
    day_out = dayworkout.split("-")
    day_in = dayworkin.split("-")
    
    # Create empty auxialiary list 
    hostlist = []
    desclist = []
    glpiticketlist = []
    triggeridlist = []
    datelist = []
    
    events = 0

    # Actions to notification (Telegram, E-mail, Call...)
    for event in sqlresult:
        TriggerCheck = zbxapi.trigger.get(triggerids=event[0], selectHosts=['host'])
        pattern = "('lastchange':) '(\d+)'"
        lastchange = re.search(pattern, str(TriggerCheck))
        triggerid = event[0]
        triggertime = event[1]
        triggerdesc = event[2]
        triggerhost = event[3]
        eventdate = event[4]
        IssueDurationTime = int(timestampnow) - int(lastchange.group(2))
        if int(lastchange.group(2)) == event[1] and IssueDurationTime > int(cfg.get('general', 'alert_time')):
            if cfg.get('general', 'tck_creation').casefold() == "true":
                #print("Glpi...")
                glpiticketid = glpi_crt.create_ticket(triggerdesc, triggerhost)
                glpiticketlist.append(glpiticketid)
            if cfg.get('general', 'zbx_ack').casefold() == "true":
                #print("Ack...")
                zbx_ack.set_zbx_acknowledge(triggerid, glpiticketid, triggertime)
            hostlist.append(triggerhost)
            desclist.append(triggerdesc)
            triggeridlist.append(triggerid)
            datelist.append(eventdate)
            if cfg.get('general', 'tlg_notify').casefold() == "true":
                zbx_teleg.create_telegram_msg(glpiticketid, triggerdesc, triggerhost)
                print(timenow, ("- Telegram API: Sent notification from event {t}.").format(t=event[0]))
            mysqlupdate()
            events += 1
        elif int(lastchange.group(2)) != event[1]:
            print(timenow, ("- Zabbix API: Event {t} recovered. Marking as seen...").format(t=event[0]))
            mysqlupdate()

    timenow_hour = timenow.hour
    datetoday = date.today() 

    #sqlholidays = """SELECT HolidayDate FROM zp_holidays"""
    #database.mycursor.execute(sqlholidays)
    #sqlholidaysresult = database.mycursor.fetchall()

    #holidays = []
    #for h in sqlholidaysresult:
    #    holidays.append(str(h[0]))
    
    if events > 0:
        if dayweek in range(int(day_in[0]), int(day_in[1])) and \
                int(time_in[0]) <= timenow_hour <= int(time_in[1]):
                #and str(datetoday) not in str(holidays):
            if cfg.get('general', 'mail_notify').casefold() == "true":
                msg_crt.create_msg_mail(triggeridlist, hostlist, desclist, datelist)
                mail_send.send_mail(triggeridlist)
                print(timenow, ("- SMTP Server: Sent mail to event {t}.").format(t=event[0]))
        else:
            if cfg.get('general', 'call_notify').casefold() == "true":
                #print("Creating...")
                msg_crt.create_msg_file(hostlist, desclist, triggeridlist, glpiticketlist)
                #print("Converting...")
                zbx_conv.tts_converter(triggeridlist)
                time.sleep(5.0)
                asterisk.make_call(triggeridlist)
                print(timenow, "- Asterisk API: The call was done.")
    
    print(timenow, "- Control Manager: Nothing to do anymore. Waiting for issues...")

# Function manager process polling
if __name__ == '__main__':
    sleep(30)
    zp_manager()
    while True:
        sleep(int(cfg.get('general', 'manager_polling')))
        zp_manager()

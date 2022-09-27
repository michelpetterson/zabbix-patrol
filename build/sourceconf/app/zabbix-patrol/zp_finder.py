# coding=utf-8
from pyzabbix import ZabbixAPI
import datetime
import time
from time import sleep
from datetime import date
from configparser import ConfigParser
import database

# current date and time
timenow = datetime.datetime.now()

print(timenow, "- Control Finder: Starting zp_finder process...")

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

def zp_finder():
    
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
    
    # current date and time
    timenow = datetime.datetime.now()
    timepast = timenow - datetime.timedelta(0, 600)
    timestamp = datetime.datetime.timestamp(timepast)
    currenttime = int(timestamp)
    
    datetoday = date.today()
    dayweek = datetoday.weekday()
    
    # Load parameters from worktime
    dayworkin = cfg.get('workday', 'in_office_days')
    dayworkout = cfg.get('workday', 'out_office_days')
    day_out = dayworkout.split("-")
    day_in = dayworkin.split("-")
    
    in_office = cfg.get('worktime', 'in_office_time')
    time_in = in_office.split("-")
    out_office = cfg.get('worktime', 'out_office_time')
    time_out = out_office.split("-")
    
    timenow_hour = timenow.hour
    
    # Print zabbix connection 
    print(timenow, "- Zabbix API: Connected to Version %s" % zbxapi.api_version())
    print(timenow, "- Zabbix API: Checking current zabbix alerts...")
    
    def get_triggers(triggers_, unack_triggers_):
    
        unack_trigger_ids = [t['triggerid'] for t in unack_triggers_]
        for t in triggers_:
            t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
                else False
    
        # Print a list containing only "tripped" triggers
        trigger_attr = ()
    

        sqlevents="""SELECT TriggerZbxHost,TriggerZbxLastChange from zp_events \
                       WHERE TriggerChecked = 'No'"""
        database.mycursor.execute(sqlevents)
        sqleventsresult = database.mycursor.fetchall()

        sqlLast = []
        sqlHost = []

        for event in sqleventsresult:
            sqlLast.append(event[1])
            sqlHost.append(event[0])

        for t in triggers_:
            if int(t['value']) == 1:
                if str(t['lastchange']) not in sqlLast and t['hosts'] not in sqlHost:
                    trigger_attr = (t['triggerid'],t['lastchange'],t['description'])
                    hostattr = t['hosts']
                    for x in hostattr:
                        host = x['host']
                    trigger_attr = trigger_attr + (host,)
                    sql = "INSERT INTO zp_events (TriggerZbxId, TriggerZbxLastChange, TriggerZbxDesc, " \
                          "TriggerChecked, TriggerZbxHost) " \
                          "VALUES (%s, %s, %s, %s, %s)"
                    val = (trigger_attr[0], trigger_attr[1], trigger_attr[2], "No", trigger_attr[3])
                    database.mycursor.execute(sql, val)
                    database.db.commit()
                    print(timenow, "- Zabbix API: Event:", t)
    
    if dayweek in range(int(day_in[0]), int(day_in[1]) + 1) and int(time_in[0]) <= timenow_hour < int(time_in[1]):
        # Get a list of all issues (AKA tripped triggers)
        triggers = zbxapi.trigger.get(only_true=1, skipDependent=1, monitored=1, active=1,
                                      lastChangeSince=currenttime, min_severity=4,  # Trigger severity: high
                                      output='extend', expandDescription=1, selectHosts=['host'],groupids=int(cfg.get('zabbix', 'groupid_24x7')))
    
        # Do another query to find out which issues are Unacknowledged
        unack_triggers = zbxapi.trigger.get(only_true=1, skipDependent=1, monitored=1, active=1,
                                            lastChangeSince=currenttime, min_severity=4, # Trigger severity: high
                                            output='extend', expandDescription=1, selectHosts=['host'],groupids=int(cfg.get('zabbix', 'groupid_24x7')),
                                            withLastEventUnacknowledged=1)
    
        get_triggers(triggers, unack_triggers)
    else:
        # Get a list of all issues (AKA tripped triggers)
        triggers = zbxapi.trigger.get(only_true=1, skipDependent=1, monitored=1, active=1,
                                      lastChangeSince=currenttime, min_severity=4,  # Trigger severity: high
                                      output='extend', expandDescription=1, selectHosts=['host'],
                                      groupids=int(cfg.get('zabbix', 'groupid_24x7')))  # Filter by zabbix group "monitoramento central"
    
        # Do another query to find out which issues are Unacknowledged
        unack_triggers = zbxapi.trigger.get(only_true=1, skipDependent=1, monitored=1, active=1,
                                            lastChangeSince=currenttime, min_severity=4, # Trigger severity: high
                                            output='extend', expandDescription=1, selectHosts=['host'],
                                            groupids=int(cfg.get('zabbix', 'groupid_24x7')),  # Filter by zabbix group "monitoramento central"
                                            withLastEventUnacknowledged=1)
    
        get_triggers(triggers, unack_triggers)
    
    print(timenow, "- Control Finder: Nothing to do anymore. Waiting for next cycle...")

# Function finder process polling
if __name__ == '__main__':
    zp_finder()
    while True:
        sleep(int(cfg.get('general', 'finder_polling')))
        zp_finder()

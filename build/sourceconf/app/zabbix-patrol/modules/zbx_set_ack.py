from pyzabbix import ZabbixAPI
from configparser import ConfigParser
import datetime
from datetime import date
import time

timenow = datetime.datetime.now()

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

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


def set_zbx_acknowledge(triggerid, glpiticketid, triggertime):
    eid = []

    timestamp = triggertime - 100
    events = zbxapi.event.get(only_true=1,
                              limit=5,
                              objectids=triggerid,
                              skipDependent=1,
                              monitored=1,
                              active=1,
                              time_from=timestamp,
                              output='extended',
                              expandDescription=1)

    for e in events:
        eid.append(e['eventid'])
    #print(eid)

    for a in eid:
        #print(a)
        zbxapi.event.acknowledge(eventids=a,
                                 message='Chamado #{t}'.format(t=glpiticketid))
                                 #action=6)
        print(timenow, "- Zabbix API: The event " +  (a) + " was acknowledged.")

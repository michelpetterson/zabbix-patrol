# coding=utf-8

from pyzabbix import ZabbixAPI

# Set variables to connection with Zabbix API
ZbxServer = "https://zabbix.domain.com"
ZbxUsername = ""
ZbxPassword = ""

# Zabbix API Server
zbxapi = ZabbixAPI(ZbxServer)

# Zabbix API Authentication
zbxapi.login(ZbxUsername, ZbxPassword)

# Specify a timeout (in seconds)
zbxapi.timeout = 5.1

print("Connected to Zabbix API Version %s" % zbxapi.api_version())

# Get a list of all issues (AKA tripped triggers)
triggers = zbxapi.hostgroup.get(only_true=1,
                              skipDependent=1,
                              groupids=495,
                              monitored=1,
                              active=1,
                              output='extend')
                              #triggerids=15857,
                              # lastChangeSince=1564421831,
                              #min_severity='high',
                              # selectLastEvent=["eventid", "acknowledged", "objectid", "clock", "ns"],
                              # sortfield='lastchange',
                              #expandDescription=0)
                              # selectHosts=['host'])

for item in triggers:
    print(item)

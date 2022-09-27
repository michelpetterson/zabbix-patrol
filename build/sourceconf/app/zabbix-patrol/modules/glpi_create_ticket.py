# coding=utf-8
import os
import json
from glpi import GLPI
import datetime
from datetime import date
import time
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

def create_ticket(triggerdesc, triggerhost):
    # GLPI Api url
    url = cfg.get('glpi', 'glpi_api_url')

    # Generate in Configuration -> General -> API
    app_token = cfg.get('glpi', 'glpi_app_token')

    # Generate in User Preference
    api_token = cfg.get('glpi', 'glpi_api_token')

    # Get date and time now
    #timenow = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")
    timenow = datetime.datetime.now()

    glpi = GLPI(url, app_token, api_token)

    ticket_message = "{n} - {h} - {t}".format(n=timenow, h=triggerhost, t=triggerdesc)
    ticket_subject = "[Zabbix|Sobreaviso] - Incidente no servidor {s}".format(s=triggerhost)

    ticket_payload = {
    'name': ticket_subject,
    'groups_id': 10,
    'content': ticket_message
    }

    ticket_dict = glpi.create(item_name='ticket', item_data=ticket_payload)
    #print(ticket_dict)
    #if isinstance(ticket_dict, dict):
    #    print("The create ticket request was sent.")

    TicketCreated = json.dumps(ticket_dict,
                      indent=4,
                      separators=(',', ': '),
                      sort_keys=True)

    TicketID = json.loads(TicketCreated)
    getid = (TicketID['id'])
    print(timenow, "- GLPI API: Ticket " + str(getid) + " was created.")
    return getid

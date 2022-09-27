import socket
import datetime
from datetime import date
import time
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')

timenow = datetime.datetime.now()


def make_call(triggeridlist):
    host = cfg.get('asterisk', 'host')
    port = 5038 

    p = """Action: login
Events: On
Username: %(username)s
Secret: %(password)s

Account: zabbix
Action: originate
Async: False
Channel: SIP/%(local_user)s@sobreaviso
WaitTime: 60
CallerId: zabbix
Exten: %(phone_to_dial)s
Context: zabbixcall
Priority: 3
Set: %(file_name)s

Action: Logoff
"""

    def click_to_call(phone_to_dial, username, password, local_user, file_name):
        pattern = p % {
                'phone_to_dial': phone_to_dial,
                'username': username,
                'password': password,
                'local_user': local_user,
                'file_name': file_name}

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        for x in pattern.split('\n'):
            #print(timenow, "- Asterisk API: ", x)
            s.send(x.encode() + "\r\n".encode())
            if x == "":
                data = s.recv(1024)
                #print(data)
        s.shutdown(socket.SHUT_RDWR)
        print(timenow, "- Asterisk API: The callfile was sent.")

    if __name__ != '__main__':
        filename = "/tmp/issue_tid" + '_'.join(map(str, triggeridlist))
        click_to_call(phone_to_dial='s',
                      username='zabbix',
                      password='1045br',
                      local_user='6000',
                      # file_name='issue_tid{t}'.format(t=triggeridlist)
                      file_name=filename
                      )

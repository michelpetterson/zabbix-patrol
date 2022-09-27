# coding=utf-8

from ftplib import FTP
import os
import fileinput
triggerid = "54677"
import datetime
from datetime import date
import time

timenow = datetime.datetime.now()

def ftp_upload(triggerid):
    ftp = FTP()
    ftp.set_debuglevel(0)
    ftp.connect('tassadar.l1nuxc0d3.com', 21)
    ftp.login('zabbix-patrol', 'Z@bbix_2018$')

    ftp.cwd('/asterisk')

    # Fix asterisk get variable from call file.
    # localfile = '/tmp/issue_tid{t}.mp3'.format(t=triggerid)
    localfile = '/tmp/issue.mp3'

    fp = open(localfile, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()
    print(timenow, "- FTP System: File" + localfile + " uploaded.")

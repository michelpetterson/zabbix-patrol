 # coding=utf-8

import smtplib
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configparser import ConfigParser

def send_mail(triggeridlist):
    cfg = ConfigParser()
    cfg.read('config/zpconfig.ini')

    filename = "/tmp/issue_tid" + '_'.join(map(str, triggeridlist)) + ".txt"
    file = open(filename, "r")
    message = file.read()
    file.close()

    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y %H:%M")

    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """

    contacts = cfg.get('mail', 'mail_to')
    emails = contacts.split(",")

    def send():
        # config SMTP server
        host = cfg.get('mail', 'mail_host')
        port = cfg.get('mail', 'mail_port')
        smtp_user = cfg.get('mail', 'mail_user')
        smtp_pass = cfg.get('mail', 'mail_pass')

        smtp = smtplib.SMTP_SSL(host, port)
        smtp.ehlo()
        smtp.login(smtp_user, smtp_pass)

        # For each contact, send the email:
        for addr in emails:
            msg = MIMEMultipart()  # create a message

            # setup the parameters of the message
            msg['From'] = cfg.get('mail', 'mail_from')
            msg['To'] = addr
            msg['Subject'] = "Alertas de incidentes {d}".format(d=date)

            # add in the message body
            msg.attach(MIMEText(message, 'html'))

            # send the message via the server set up earlier.
            smtp.send_message(msg)
            del msg

        # Terminate the SMTP session and close the connection
        smtp.quit()
    send()
    if os.path.exists(filename):
        os.remove(filename)


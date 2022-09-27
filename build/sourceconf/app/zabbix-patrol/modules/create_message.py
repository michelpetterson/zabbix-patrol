# coding=utf-8
import datetime

from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config/zpconfig.ini')


def write_msg(msg, triggeridlist):
    filename = "/tmp/issue_tid" + '_'.join(map(str, triggeridlist)) + ".txt"
    file = open(filename, "+a")
    file.write(msg)
    file.close()


def create_msg_file(hostlist, desclist, triggeridlist, glpiticketlist):
    # check time now to select greeting message
    timenow = datetime.datetime.now()
    timenow_hour = timenow.hour
    if timenow_hour < 12:
        greeting = 'Bom dia'
    elif 12 <= timenow_hour < 18:
        greeting = 'Boa tarde'
    else:
        greeting = 'Boa noite'

    contact_01 = cfg.get('contacts', 'first_contact')
    contact_02 = cfg.get('contacts', 'second_contact')
    contact_03 = cfg.get('contacts', 'third_contact')
    contact_04 = cfg.get('contacts', 'fourth_contact')

    message = ["<speak version='1.0'><prosody rate='-5%'>Olá! {g} {a}, tudo bem? Estou ligando para "
               "informar ".format(g=greeting, a=contact_01)]
    if len(hostlist) > 2:
        message.append("os seguintes incidentes: ")
        for host, desc in zip(hostlist, desclist):
            message.append("rost {h} com alerta {d}.".format(h=host, d=desc))
        message.append(" Os números dos chamados gerados foram: <say-as interpret-as='digits'>{n}"
                       "</say-as>. </prosody></speak>".format(n=', '.join(map(str, glpiticketlist))))
    else:
        message.append("o seguinte incidente: ")
        message.append("rost {h} com alerta {d}.".format(h=hostlist[0], d=desclist[0]))
        message.append("O número do chamado gerado foi: <say-as interpret-as='digits'>{n}</say-as>. Até mais! Tchau!"
                       "</prosody></speak>".format(n=glpiticketlist[0]))
    msg = ' '.join(message)
    write_msg(msg, triggeridlist)


def create_msg_mail(triggeridlist, hostlist, desclist, datelist):

    msg = """\
    <html>
    <head>
        <style>
            /* Table Format */
            .TableFormat {
                background-color: #eaedf1;
                border-spacing: 0;
            }
            .TableFormat td{
                border: 1px solid #777;
                margin: 0 !important;
                padding: 2px 3px;
            }
            .TableFormat thead {
                background-color: #5e267d;
                color: #FFF;
            }
            .TableFormat thead td {
                font-weight: bold;
                font-size: 13px;
            }
        </style>
    </head>
        <h1 style="color: #984bc3;">Lista de incidentes:</h1>
        <table class="TableFormat" style="width: 586px;">
            <thead>
                <tr>
                    <td>Data/Hora</td>
                    <td>Host</td>
                    <td>Trigger</td>
                </tr>
            </thead>
            <tbody>"""
    write_msg(msg, triggeridlist)

    for date, host, desc in zip(datelist, hostlist, desclist):
        msg = """
                <tr>
                    <td>&nbsp;{t}</td>
                    <td>&nbsp;{h}</td>
                    <td>&nbsp;{d}</td>
                </tr>""".format(t=date, h=host, d=desc)
        write_msg(msg, triggeridlist)

    msg = """
            </tbody>
        </table>
    </html>"""
    write_msg(msg, triggeridlist)

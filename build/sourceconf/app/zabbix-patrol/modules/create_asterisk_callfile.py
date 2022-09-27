# coding=utf-8
#import time, os, pwd


def create_callfile(triggerid):

    temp_dir = "/tmp/"
    callfile = "issue_tid" + str(triggerid) + ".call"
    #callfile = "issue.call"
    startcallfile = temp_dir + callfile
    end_dir = "/var/spool/asterisk/outgoing/"
    endcallfile = end_dir + callfile

    #write file to disk
    scf = open(startcallfile,"w")
    scf.write("Channel: SIP/6001@michel" + "\n")
    scf.write("MaxRetries: 3\n")
    scf.write("Callerid: 6111" + "\n")
    scf.write("RetryTime: 60\n")
    scf.write("WaitTime: 30\n")
    scf.write("Async: False\n")
    scf.write("Events: True\n")
    scf.write("Context: zabbixcall" + "\n")
    scf.write("Extension: s" + "\n")
    scf.write("Priority: 1")
    scf.close()

    #change file permission
    #os.chmod(startcallfile,0o755)
    #os.chown(startcallfile, pwd.getpwnam(os.environ['USER']).pw_uid, pwd.getpwnam(os.environ['USER']).pw_gid)

    #hour-minute-second-month-day-year (example: 02-10-00-09-27-2007)
    #if asteriskParams['touchtime'] != "":
    #    ctime = time.mktime(datetime.datetime.strptime(asteriskParams['touchtime'], "%H:%M:%S-%m-%d-%Y").timetuple())
    #    os.utime(startcallfile,ctime,ctime,) #change file time to future date

    #move file to /var/spool/asterisk/outgoing
    #os.rename(startcallfile, endcallfile)


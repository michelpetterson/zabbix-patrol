import requests
from datetime import datetime
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from database import *

try:
    url_nac = "https://dadosbr.github.io/feriados/nacionais.json"
    url_uf = "https://raw.githubusercontent.com/joaopbini/feriados-brasil/master/dados/feriados/estadual/json/2021.json"
    nac_request = requests.get(url_nac)
    uf_request = requests.get(url_uf)

    holidays = []
    nac_dic = {}
    uf_dic = {}

    # Sql query to get holiday dates

    sqldates = """SELECT HolidayDate FROM zp_holidays"""
    mycursor.execute(sqldates)
    sqlresult = mycursor.fetchall()

    for uf_holiday in uf_request.json():
        if uf_holiday['uf'] == "BA":
            uf_date = datetime.strptime(uf_holiday['data'], '%d/%m/%Y').date()
            uf_dic = {"date": uf_date, "name": uf_holiday['nome'], "desc": uf_holiday['descricao']}
            holidays.append(uf_dic)

    for nac_holiday in nac_request.json():
        if nac_holiday['date'] != "":
            holidaydate = nac_holiday['date'] + "/" + str(datetime.now().year)
            nac_date = datetime.strptime(holidaydate, '%d/%m/%Y').date()
            nac_dic = {"date": nac_date, "name": nac_holiday['title'], "desc": nac_holiday['description']}
            holidays.append(nac_dic)


    # Insert dates in table zp_holidays from database
    dates=[]
    for d in sqlresult:
        dates.append(str(d[0]))

    for dic in holidays:
        if str(dic['date']) not in str(dates):
            sql = "INSERT INTO zp_holidays (HolidayDate, HolidayName, HolidayDesc) " \
                  "VALUES (%s, %s, %s)"
            val = (dic['date'], dic['name'], dic['desc'])
            mycursor.execute(sql, val)
            db.commit()

    # Quaery added records

    sql = "SELECT * FROM zp_holidays"
    mycursor.execute(sql)
    sqlresult = mycursor.fetchall()

    for row in sqlresult:
        print("=============== Feriado: =================")
        print(row[1], "-", row[2])
        print("==========================================")

except mysql.Error as error:
    print("Error while working with MySQL", error)
finally:
    if (db):
            db.close()

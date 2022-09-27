# coding=utf-8
import mysql.connector

db = mysql.connector.connect(
    host="zp_database",
    port="3306",
    database="zpdb",
    user="zpuser",
    passwd="Zp2o18_",
    autocommit=True
)

mycursor = db.cursor()


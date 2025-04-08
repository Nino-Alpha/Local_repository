#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logDHT.py
#
#  Developed by Marcelo Rovai, MJRoBot.org @ 10Jan18
#  
#  Capture data from a DHT22 sensor and save it on a database

import time
import sqlite3
import Adafruit_DHT

dbname='sensorsData.db'
#sampleFreq = 60 time in seconds

# get data from DHT sensor
def getDHTdata():	
	
	DHT11Sensor = Adafruit_DHT.DHT11
	DHTpin = 17
	hum, temp = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin)
	
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

# log sensor data on database
def logData (temp, hum):
	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()	
	curs.execute("INSERT INTO DHT_data values(datetime('now','localtime'), (?), (?))", (temp, hum)) # modify : localtime
	conn.commit()
	conn.close()
	
def getFreqdata():	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT * FROM Sample_freq ORDER BY timestamp DESC LIMIT 1")
	row = curs.fetchone()
	if row:
		freq = row[1]
		return freq
	return None

# function ： display database data (nlast input)
def displayData():
	conn=sqlite3.connect('sensorsData.db')
	curs=conn.cursor()
	print ("\nLast DHT Data logged on database:\n")#显示温湿度的输出
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		print (str(row[0])+" ==> Temp = "+str(row[1])+"	Hum ="+str(row[2]))

	print ("\nLast Freq Data logged on database:\n")#增加显示频率的输出
	for row in curs.execute("SELECT * FROM Sample_freq ORDER BY timestamp DESC LIMIT 1"):
		print (str(row[0])+" ==> Freq = "+str(row[1]))

# main function
def main():
	while True:
		sampleFreq = getFreqdata()
		temp, hum = getDHTdata()
		logData (temp, hum)
		displayData()   #服务器运行期间，也输出数据以方便监控。
		time.sleep(sampleFreq)

# ------------ Execute program 
if __name__ == '__main__':
	main()


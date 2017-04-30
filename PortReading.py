
'''
    Author: Ming YUE
    Date: 4/27/2017
    Discerption: This program is about recieving the package from the sensor, reading the information and storing it in MySQL.
    
'''

import serial
import time
import datetime
import MySQLdb

#changing ascii to hex
def hexShow(argv):
    result=''
    hLen=len(argv)
    for i in xrange(hLen):
        hvol=ord(argv[i])
        hhex='%02x'%hvol
        result+=hhex
    return result




#connecting to mysql
conn=MySQLdb.connect(host='localhost',user='root',passwd='root123456',db='Xbee')  //change it with your own information of the MySQL
cursor=conn.cursor()
sql="""CREATE TABLE RECIEVE( #create tables
       Source CHAR(20) NOT NULL,
       Info CHAR(100) NOT NULL,
       Date CHAR(20) NOT NULL,
       Time CHAR(20) NOT NULL)"""
cursor.execute(sql)


t=serial.Serial('/dev/cu.usbserial-A8003LRA',38400) #open the serial
i=1
x='7e'
while i<20:
    str=t.read(1)
    data=hexShow(str)
    if data=='7e':
        sqr=t.read(2)
        data2=hexShow(sqr)
        value=int(data2,16)
        j=0
        data=t.read(1)
        data=t.read(8)
        source=hexShow(data) #get the source adress
        data=t.read(1)
        data=t.read(5)
        #data=t.read(value-10)
        data=t.read(value-15) #get the data in the frame
        #print data
        package=data
        print "Recieved Data:"+package
        #time1=time.strftime("%m/%d/%Y %H:%M:%S")
        date2=time.strftime("%m/%d/%Y") #get date
        time2=time.strftime("%H:%M:%S") #get time
        #print data
        sql="INSERT INTO RECIEVE(Source,Info,Date,Time)\
             VALUES('%s','%s','%s','%s')"%\
             (source,package,date2,time2)
        #print package
        cursor.execute(sql)
        conn.commit() #execute it in mysql
        i=i+1

conn.close() #close the connections
t.close()











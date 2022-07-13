import serial
import csv
import mysql.connector
from datetime import datetime
from datetime import date
def getsensordata(inspection_id,wt,token,Moist):
    humidity =''
    tempc =''
    tempfar =''
    capacitance = ''
    sensor5 =''
    sensor4 =''
    sensor3 = ''
    sensor2 =''
    sensor1= ''
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H.%M.%S")
    combined = str(today) + ' ' + str(current_time)
    print(Moist)
    try:
        ser = serial.Serial('com6',9600)
        ser.flushInput()
        for i in range (1,30):
                ser_bytes = ser.readline()
                decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                #print(decoded_bytes)
                with open("serial_dat.csv",'a',newline='') as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow([decoded_bytes])
        with open("serial_dat.csv","r") as file: 
            data = file.readlines()
            for r in range (1,10):    
                decoded_bytes = data[-r] 
                #print (decoded_bytes,r)
                
                #print(inspection_id)
                
                
                if (decoded_bytes.find("Humidity") != -1):
                    if (humidity == ''):
                        humidity  = decoded_bytes[-10:]
                        humidity =humidity.strip()
                    
                    
                        #print(humidity)
                   
                elif (decoded_bytes.find("Celsius") != -1):
                    if (tempc == ''):
                        tempc = decoded_bytes[-8:]
                        tempc = tempc.strip()
                        #print(tempc)
                    
                elif (decoded_bytes.find("Fahrenheit") != -1):
                    if (tempfar == ''):
                        tempfar = decoded_bytes[-8:]
                        tempfar = tempfar.strip()
                        #print(tempfar)
                elif (decoded_bytes.find("average persentage") != -1):
                    if (capacitance == ''):
                        capacitance = decoded_bytes[-8:]
                        capacitance= capacitance.strip()
                        #print(capacitance)
                elif (decoded_bytes.find("1st sensor") != -1):
                    if (sensor1 == ''):
                        sensor1 = decoded_bytes[-7:]
                        sensor1= sensor1.strip()
                        #print(sensor1)
                elif (decoded_bytes.find("2nd sensor") != -1):
                    if (sensor2 == ''):
                        sensor2 = decoded_bytes[-7:]
                        sensor2= sensor2.strip()
                        #print(sensor2)
                elif (decoded_bytes.find("3rd sensor") != -1):
                    if (sensor3 == ''):
                        sensor3 = decoded_bytes[-7:]
                        sensor3= sensor3.strip()
                        #print(sensor3)
                elif (decoded_bytes.find("4th sensor") != -1):
                    if (sensor4 == ''):
                        sensor4 = decoded_bytes[-7:]
                        sensor4= sensor4.strip()
                        #print(sensor4)
                elif (decoded_bytes.find("5th sensor") != -1):
                    if (sensor5 == ''):
                        sensor5 = decoded_bytes[-7:]
                        sensor5= sensor5.strip()
                        #print(sensor5)
                        
            #print(sensor4,sensor5)
            if sensor4 == '':
                sensor4 =0
            if sensor5 == '':
                sensor5 =0
    except serial.SerialException as e:
        
        sensor1 =0
        sensor2 =0
        sensor3 =0
        sensor4 =0
        sensor5 =0
        humidity = str(Moist)  + '%'          
    weight = str(wt) +" KG"
    #print(weight)
    connection = mysql.connector.connect(user='root', password='Password123#$',
                              host='127.0.0.1',
                              database='tea_project')
    cursor = connection.cursor() 
    sql_select_Query ="insert into sensor_data (inspection_id,date,humidity,tempc,tempf,capacitance,weight,sensor1,sensor2,sensor3,sensor4,sensor5,token) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (inspection_id,combined,humidity,tempc,tempfar,capacitance,weight,sensor1,sensor2,sensor3,sensor4,sensor5,token)
    cursor.execute(sql_select_Query,val)
    connection.commit()
    cursor.close
    connection.close()
                       
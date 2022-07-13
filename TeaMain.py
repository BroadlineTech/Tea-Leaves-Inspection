import pandas as pd
import sys
import cv2
import glob
import random
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget,QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import mysql.connector
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
from datetime import date
import matplotlib
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
import serialpage
import subprocess
from datetime import datetime
from datetime import date
import os
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
#import datetime
from threading import Thread
from queue import Queue
import numpy as np
import imutils
from PIL import Image
from threading import Thread
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
from PyQt5.QtCore import QSize
import qrcode 
import matplotlib.pyplot as plt
#import graphgen
#import qrgenerator
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np


index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if ret:
                
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Tea Leaves Inspection'
        self.setWindowIcon(QtGui.QIcon('tealeaf.jpg'))
        self.left = 25
        self.top = 75
        self.width = 2000
        self.height = 1500
        self.logic =0
        self.value =1
        
        self.initUI()
    def setImage(self, image):
        self.labelcam.setPixmap(QPixmap.fromImage(image))
    def click_event(self):
        import glob
        RefSensor1A =0
        RefSensor1B =0
        RefSensor1C =0
        RefSensor1D = 0
        RefSensor2A =0
        RefSensor2B =0
        RefSensor2C =0
        RefSensor2D = 0
        RefSensor3A =0
        RefSensor3B =0
        RefSensor3C =0
        RefSensor3D = 0
        RefSensor4A =0
        RefSensor4B =0
        RefSensor4C =0
        RefSensor4D = 0
        RefSensor5A =0
        RefSensor5B =0
        RefSensor5C =0
        RefSensor5D = 0
        plt.clf()  
        if self.textbox1.text() == '':
            QMessageBox.information(self, 'Message - Oops', "Weight cannot be empty!!", QMessageBox.Ok, QMessageBox.Ok)
            self.textbox1.setFocus()
            return
        if self.texttkn.text() =='':
            QMessageBox.information(self, 'Message - Oops', "Token # cannot be empty!!", QMessageBox.Ok, QMessageBox.Ok)
            self.texttkn.setFocus()
            return
        ret = QMessageBox.question(self, 'MessageBox', "Has the image been saved?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            return
        else:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            connection = mysql.connector.connect(user='root', password='Password123#$',
                              host='127.0.0.1',
                              database='tea_project')
            cursor = connection.cursor()
            cursor.execute("select count(distinct Grade) as ct from ref_data")
            for x in cursor.fetchall():
                row = x[0]
                #print (row)
            if row != 4:
                QMessageBox.information(self, 'Message - Oops', "Not Enough Grades taught ", QMessageBox.Ok, QMessageBox.Ok)
                return
            
            list_of_files = glob.glob(r'C:\hannah\demo\teaimages\*.jpg') 
            latest_file = max(list_of_files, key=os.path.getctime)
            img = cv2.imread(latest_file, 1)
            #img = cv2.imread('tealeaves06.jpg', 1)
            # checking for left mouse clicks
            #if event == cv2.EVENT_LBUTTONDOWN:
            coordinates = []
            A=0
            B=0
            C =0
            D =0
            RedA = 0
            RedB =0
            Redc =0
            GreenA =0
            GreenB =0
            Greenc =0
            BlueA =0
            BlueB =0
            BlueC =0
            pieval =0
            list1 = []
            now = datetime.now()
            today = date.today()
            current_time = now.strftime("%H.%M.%S")
            for i in range (0,100):
                x = random.randint(50,500)
                y = random.randint(70,400)
                #print(x, ' ', y)
                font = cv2.FONT_HERSHEY_SIMPLEX
                b = img[y, x, 0]
                g = img[y, x, 1]
                r = img[y, x, 2]
                #print (r,g,b)
                text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)  
                #print(text)
                if (r != 255) and (g != 255) and (b!= 255):
                    RedA = 0
                    GreenA =0
                    BlueA =0
                    RedB = 0
                    GreenB =0
                    BlueB =0
                    RedC = 0
                    GreenC =0
                    BlueC =0
                    RedD = 0
                    GreenD =0
                    BlueD =0
                    
                    sql_select_QueryA ="select Red,Green,Blue,count(*) from ref_data where Grade = 'Grade A'"
                    cursor.execute(sql_select_QueryA)
                    
                    for x in cursor.fetchall():
                        #resultloc = cursor.fetchall()
                        countA = int(x[3])
                        RedA = int(x[0]) + RedA
                        GreenA = int(x[1]) + GreenA
                        BlueA = int(x[2]) + BlueA
                        #print(RedA,GreenA,BlueA,countA)
                    RedA = int(RedA)/int(countA)
                    GreenA =int(GreenA)/int(countA)
                    BlueA = int(BlueA)/int(countA)
                    sql_select_QueryB ="select Red,Green,Blue,count(*) from ref_data where Grade = 'Grade B'"
                    cursor.execute(sql_select_QueryB)
                    for x in cursor.fetchall():
                        #resultloc = cursor.fetchall()
                        countB = int(x[3])
                        RedB = int(x[0]) + RedB
                        GreenB = int(x[1]) + GreenB
                        BlueB = int(x[2]) + BlueB
                    RedB = int(RedB)/int(countB)
                    GreenB =int(GreenB)/int(countB)
                    BlueB = int(BlueB)/int(countB)   
                    sql_select_QueryC="select Red,Green,Blue,count(*) from ref_data where Grade = 'Grade C'"
                    cursor.execute(sql_select_QueryC)
                    for x in cursor.fetchall():
                        #resultloc = cursor.fetchall()
                        countC = int(x[3])
                        RedC = int(x[0]) + RedC
                        GreenC = int(x[1]) + GreenC
                        BlueC = int(x[2]) + BlueC
                    RedC = int(RedC)/int(countC)
                    GreenC =int(GreenC)/int(countC)
                    BlueC = int(BlueC)/int(countC) 
                    sql_select_QueryD="select Red,Green,Blue,count(*) from ref_data where Grade = 'Grade D'"
                    cursor.execute(sql_select_QueryD)
                    for x in cursor.fetchall():
                        #resultloc = cursor.fetchall()
                        countD = int(x[3])
                        RedD = int(x[0]) + RedD
                        GreenD = int(x[1]) + GreenD
                        BlueD = int(x[2]) + BlueD
                    RedD = int(RedD)/int(countD)
                    GreenD =int(GreenD)/int(countD)
                    BlueD = int(BlueD)/int(countD) 
                    
                    
                    
                    #if (r != 255) and (g != 255) and (b!= 255):
                    '''   
                    print(RedA,GreenA,BlueA)
                    print(RedB,GreenB,BlueB)
                    print(RedC,GreenC,BlueC)
                    print(RedD,GreenD,BlueD)
                    '''

                    if ((r in range ((int(RedA)-10),(int(RedA)+10))) and (g in range ((int(GreenA)-10),(int(GreenA)+10))) and (b in range ((int(BlueA)-10),(int(BlueA)+10)))):
                        A = A +1
                    elif ((r in range ((int(RedB)-20),(int(RedB)+20))) and (g in range ((int(GreenB)-20),(int(GreenB)+20))) and (b in range ((int(BlueB)-20),(int(BlueB)+20)))):
                        B = B +1
                    elif ((r in range ((int(RedD)-20),(int(RedD)+20))) and (g in range ((int(GreenD)-20),(int(GreenD)+20))) and (b in range ((int(BlueD)-20),(int(BlueD)+20)))):
                        D =D+1
                    elif ((r in range ((int(RedC)-20),(int(RedC)+20))) and (g in range ((int(GreenC)-20),(int(GreenC)+20))) and (b in range ((int(BlueC)-20),(int(BlueC)+20)))):
                        C = C +1  
                   
                    
            list1 = [A,B,C,D]
            m=(A+B+C+D)/100
            A = round(A/m,2)
            B = round(B/m,2)
            C = round(C/m,2)
            D = round(D/m,2)
            '''
            print (list1)
            print ("A+ quality is " + str(A) + "%")
            print ("B quality is " + str(B) + "%")
            print ("C quality is " + str(C) + "%")
            
            print ("Other quality is " + str(D) + "%")
            print("Overall good quality percentage is (" + str(A+B+C) + "%)")
            print ("Rejected percentage is (" + str(D)+ "%)")   
            '''
            '''  
            objects = ('A', 'B', 'C', 'D(Others)')
            y_pos = np.arange(len(objects))
            performance = [A,B,C,D]
            plt.figure(figsize=(5,4))
            plt.ylim(0,100)
            #plt.text(plt.bar.get_x() + plt.bar.get_width()/2.0, yval, int(yval), va='bottom') #va: vertical alignment y positional argument
            plt.bar(y_pos, performance, align='center', color = '#006400')
            plt.xticks(y_pos, objects)
            
            for i in range(len(performance)):
                plt.text(i,performance[i],s="{}%".format(performance[i],ha='center'))
            plt.ylabel('Percentage Accepted (%)')
            plt.xlabel('Grades')
            plt.title('Tea Leaves Inspection Result')
            #plt.figure(figsize=(10,10)) 
            #plt.show()
            plt.savefig('Inspection.png')
            plt.clf()
            self.im = QPixmap("inspection.png")
            
            self.labelpie.setPixmap(self.im)
            '''
            sql_select_Queryloc ="select location_id from location where location='" + self.combo_box1.currentText() + "'" 
            cursor.execute(sql_select_Queryloc)
            for x in cursor.fetchall():
                #resultloc = cursor.fetchall()
                locid = x[0]
                #print (locid)
            loc = self.combo_box2.currentText()
            #print(loc)
            sql_select_Queryfarm ="select farmer_id from farmers_detail where farmername='" + self.combo_box2.currentText() + "' and location_id =(select location_id from location where location='" + self.combo_box1.currentText() + "')"  
            cursor.execute(sql_select_Queryfarm)
            for f in cursor.fetchall():
              farmid = f[0]
            
            #dt = datetime.datetime(today)
            #tm = datetime.time(current_time)
            #combined = dt.combine(dt, tm)
            combined = str(today) + ' ' + str(current_time) 
            sql_selectid_query = "select max(inspection_id) as inspection_id from inspection_detail"
            cursor.execute (sql_selectid_query)
            for x in cursor.fetchall():
                if x[0] is None:
                    inspid = 1
                else:
                    inspid = x[0] +1
            sql_insert_inspdetail = "insert into inspection_detail (inspection_id,location_id,Date,farmer_id,A,B,C,D) values (%s,%s,%s,%s,%s,%s,%s,%s)" 
            #val = (%(1)s,%(combined)s,%(1)s,%('550 Farad')s,%('320 kg')s,%('18.52')s,%('25 degrees')s,%('0.0%')s,%('0.0%')s,%('8.0%')s,%('9.2%')s,%('16.8%')s,%('4.8%')s,%('51.2%')s)
            val = (inspid,locid,combined,farmid,A,B,C,D)
            #val = (1,'2022/05/05 16:26:00',1,'550 Farad','320 kg','18.52','25 degrees','0.0%','0.0%','8.0%','19.2%','16.8%','4.8%','51.2%')
            cursor.execute(sql_insert_inspdetail,val)
            connection.commit()
            
            
            
            sql_select_inspid = "select max(inspection_id) as inspection_id from inspection_detail"
            cursor.execute(sql_select_inspid)
            for n in cursor.fetchall():
              inspection_id = str(n[0])
            cursor.close
            connection.close()
            wt = self.textbox1.text()
            token = self.texttkn.text()
            if self.radio1.isChecked():
                Moist = 90
            else:
                Moist = 73
            serialpage.getsensordata(inspection_id,wt,token,Moist)
                   
            connection = mysql.connector.connect(user='root', password='Password123#$',
                              host='127.0.0.1',
                              database='tea_project')
            cursor = connection.cursor()
            
            
            sql_select_RefsensorA_Query="select sum(Tsensor1),sum(Tsensor2),sum(Tsensor3),count(*) from ref_data where Grade = 'Grade A'"
            cursor.execute(sql_select_RefsensorA_Query)
            for x in cursor.fetchall():
                countSA = int(x[3])
                RefSensor1A = int(x[0]) + RefSensor1A
                RefSensor2A = round((int(x[1]) + RefSensor2A),2)
                RefSensor3A = int(x[2]) + RefSensor3A
                #RefSensor4A = int(x[3]) + RefSensor4A
                #RefSensor5A = int(x[4]) + RefSensor5A
            RefSensor1A = round(int(RefSensor1A)/int(countSA),2)
            RefSensor2A = round(int(RefSensor2A)/int(countSA),2)
            RefSensor3A = round(int(RefSensor3A)/int(countSA),2)
            #print (RefSensor1A,RefSensor2A,RefSensor3A)
           # RefSensor4A = int(RefSensor4A)/int(countSA)
            #RefSensor5A = int(RefSensor5A)/int(countSA)
            
            sql_select_RefsensorB_Query="select sum(Tsensor1),sum(Tsensor2),sum(Tsensor3),count(*) from ref_data where Grade = 'Grade B'"
            cursor.execute(sql_select_RefsensorB_Query)
            for x in cursor.fetchall():
                countSB = int(x[3])
                RefSensor1B = int(x[0]) + RefSensor1B
                RefSensor2B = int(x[1]) + RefSensor2B
                RefSensor3B = int(x[2]) + RefSensor3B
                #RefSensor4B = int(x[3]) + RefSensor4B
                #RefSensor5B = int(x[4]) + RefSensor5B
            RefSensor1B = round(int(RefSensor1B)/int(countSB),2)
            RefSensor2B = round(int(RefSensor2B)/int(countSB),2)
            RefSensor3B = round(int(RefSensor3B)/int(countSB),2)
            #RefSensor4B = int(RefSensor4B)/int(countSB)
            #RefSensor5B = int(RefSensor5B)/int(countSB)
            
            sql_select_RefsensorC_Query="select sum(Tsensor1),sum(Tsensor2),sum(Tsensor3),count(*) from ref_data where Grade = 'Grade C'"
            cursor.execute(sql_select_RefsensorC_Query)
            for x in cursor.fetchall():
                countSC = int(x[3])
                RefSensor1C = int(x[0]) + RefSensor1C
                RefSensor2C = int(x[1]) + RefSensor2C
                RefSensor3C = int(x[2]) + RefSensor3C
                #RefSensor4C = int(x[3]) + RefSensor4C
                #RefSensor5C = int(x[4]) + RefSensor5C
            RefSensor1C = round(int(RefSensor1C)/int(countSC),2)
            RefSensor2C = round(int(RefSensor2C)/int(countSC),2)
            RefSensor3C = round(int(RefSensor3C)/int(countSC),2)
            #RefSensor4C = int(RefSensor4C)/int(countSC)
            #RefSensor5C = int(RefSensor5C)/int(countSC)
            
            sql_select_RefsensorD_Query="select sum(Tsensor1),sum(Tsensor2),sum(Tsensor3),count(*) from ref_data where Grade = 'Grade D'"
            cursor.execute(sql_select_RefsensorD_Query)
            for x in cursor.fetchall():
                countSD = int(x[3])
                RefSensor1D = int(x[0]) + RefSensor1D
                RefSensor2D = int(x[1]) + RefSensor2D
                RefSensor3D = int(x[2]) + RefSensor3D
                #RefSensor4C = int(x[3]) + RefSensor4C
                #RefSensor5C = int(x[4]) + RefSensor5C
            RefSensor1D = round(int(RefSensor1D)/int(countSD),2)
            RefSensor2D = round(int(RefSensor2D)/int(countSD),2)
            RefSensor3D = round(int(RefSensor3D)/int(countSD),2)
            #RefSensor4C = int(RefSensor4C)/int(countSC)
            #RefSensor5C = int(RefSensor5C)/int(countSC)
            y1= [RefSensor1A,RefSensor2A,RefSensor3A]
            y2= [RefSensor1B,RefSensor2B,RefSensor3B]
            y3= [RefSensor1C,RefSensor2C,RefSensor3C]
            y4= [RefSensor1D,RefSensor2D,RefSensor3D]
            x1 = [1,2,3]
            x2 = [1,2,3]
            x3 = [1,2,3]
            x4 = [1,2,3]
            
            
            sql_select_sensor = "select Humidity,tempc,tempf,capacitance,weight,sensor1,sensor2,sensor3,sensor4,sensor5,token from sensor_data where inspection_id =" + inspection_id 
            cursor.execute(sql_select_sensor)
            for s in cursor.fetchall():
                humidity = str(s[0])
                tempc = str(s[1])
                tempf = str(s[2])
                capacitance = str(s[3])
                weight = str(s[4])
                sensor1 = str(s[5])
                sensor2 = str(s[6])
                sensor3 = str(s[7])
                sensor4 = (s[8])
                sensor5 = (s[9])
                if sensor4 == 0: 
                  sensor4 = 0
                else:
                  sensor4 = str(s[8])
                if sensor5 ==0:
                   sensor5 = 0
                else:
                   sensor5 = str(s[9])
                 
                token = str(s[10])
            
            if sensor4 == 0:
              x = [1,2,3]
            else:
              x = [1,2,3,4,5]
            # corresponding y axis values
            #y = [39.69,38.12,39.00,41.15,53.47]
           # print (int(sensor1),int(sensor2),int(sensor3),int(sensor4),int(sensor5))
            sensor1 = float(sensor1)
            sensor2 = float(sensor2)
            sensor3 = float(sensor3)
            if sensor4 != 0:
               sensor4 = float(sensor4)
            else:
               sensor4 =0
            if sensor5 != 0:
               sensor5 = float(sensor5)
            else:
               sensor5 = 0
            if sensor4 == 0:
                y = [sensor1,sensor2,sensor3]
            else:
                y = [sensor1,sensor2,sensor3,sensor4,sensor5]
            if humidity =='':
               humidity = 'NA'
            if tempc =='':
               tempc = 'NA'
            if capacitance =='':
               capacitance = 'NA'
            '''   
            Avgsensor3 = sensor3
            Avgsensor1 = sensor1
            print(sensor4,sensor5)
            
            objects = ('Sensor 3', 'Sensor 4')
            y_pos = np.arange(len(objects))
            performance = [sensor4,sensor5]
            plt.figure(figsize=(5,4))
            plt.ylim(0,100)
            #plt.text(plt.bar.get_x() + plt.bar.get_width()/2.0, yval, int(yval), va='bottom') #va: vertical alignment y positional argument
            plt.bar(y_pos, performance, align='center', color = '#006400')
            plt.xticks(y_pos, objects)
            
            for i in range(len(performance)):
                plt.text(i,performance[i],s="{}%".format(performance[i],ha='center'))
            plt.ylabel('Percentage Accepted (%)')
            plt.xlabel('Grades')
            plt.title('Tea Leaves Inspection Result')
            #plt.figure(figsize=(10,10)) 
            #plt.show()
            plt.savefig('Inspectionsensor.png')
            plt.clf()
            self.im = QPixmap("inspectionsensor.png")
            
            self.labelpie.setPixmap(self.im)
            '''
               
            plt.figure(figsize=(5,4))
            plt.ylim(20,80)
            plt.xlim(0,6)
            
            plt.plot(x, y, color='Red', linestyle='solid', linewidth = 2,
                     marker='*', markerfacecolor='purple', markersize=10)
            plt.plot(x1, y1, color='green', linestyle='solid', linewidth = 2,
                     marker='*', markerfacecolor='black', markersize=10)
            plt.plot(x2, y2, color='blue', linestyle='solid', linewidth = 2,
                     marker='*', markerfacecolor='black', markersize=10)
            plt.plot(x3, y3, color='orange', linestyle='solid', linewidth = 2,
                     marker='*', markerfacecolor='black', markersize=10)
            plt.plot(x4, y4, color='purple', linestyle='solid', linewidth = 2,
                     marker='*', markerfacecolor='black', markersize=10)
            plt.xlabel('Sensor')
            plt.ylabel('Data')
            for i_x, i_y in zip(x, y):
                plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))  
            for i_x1, i_y1 in zip(x1, y1):
                plt.text(i_x1, i_y1, '({}, {})'.format(i_x1, i_y1)) 
            for i_x2, i_y2 in zip(x2, y2):
                plt.text(i_x2, i_y2, '({}, {})'.format(i_x2, i_y2))
            for i_x3, i_y3 in zip(x3, y3):
                plt.text(i_x3, i_y3, '({}, {})'.format(i_x3, i_y3))
            for i_x4, i_y4 in zip(x4, y4):
                plt.text(i_x4, i_y4, '({}, {})'.format(i_x4, i_y4))
            plt.title('Accoustic Sensor Data Graph')
            plt.legend(["Inspection Data","Grade A", "Grade B","Grade C","Grade D"])
            plt.savefig("graph.png")
            
            self.labelgraph.setPixmap(QPixmap("graph.png"))
            
           
            pdf = FPDF()
            pdf.add_page()
            pdf.set_xy(0, 0)
            pdf.set_font('Times', 'B', 30) 
            pdf.set_font("Times",'U',size = 30)
           # pdf.set_font(style="U")
            # create a cell
            pdf.cell(200, 10, txt = "Tea Leaves Inspection Report", 
                     ln = 1, align = 'C')
            pdf.cell(90,10, " ", 0, 2, 'Cb')
            pdf.set_font("Times", size = 22)
            pdf.cell(190,7, "DateTime:  " + str(today) + "  " + str(current_time), 0, 1, 'R')
            pdf.cell(100,10, "Token #:  " + str(token), 0, 2, 'C')
            pdf.cell(100,10, "Farmers Name:  " + str(self.combo_box2.currentText()), 0, 2, 'C')
            pdf.cell(100,10, "Location:  " + str(self.combo_box1.currentText()) , 0, 2, 'C')
            pdf.cell(100,10, "Humidity:  " + str(humidity), 0, 2, 'C')
            #pdf.cell(100,10, "Temperature:  " + tempc, 0, 2, 'C')
            pdf.cell(100,10, "Weight:  " + str(weight), 0, 2, 'C')
            pdf.cell(100,10, "Analyser Data:  " + capacitance, 0, 2, 'C')
            #pdf.cell(75,10, "Current Price:", 0, 2, 'L')
           
            #pdf.cell(40,10, " ", 0, 2, 'C')
            
            pdf.cell(-1)
            pdf.image('inspection.png',x = None, y = None, w = 0, h = 0, type = '', link = '')
            pdf.cell(-1)
            pdf.image('graph.png',x = None, y = None, w = 0, h = 0, type = '', link = '')
            pdf.output('inspection.pdf', 'F') 
            # generating a QR code using the make() function  
            qr_img = qrcode.make("inspection.pdf")  
            # saving the image file  
            qr_img.save("qr-img.jpg")
            self.labelqr.setPixmap(QPixmap("qr-img.jpg"))
            #pdf.image('qr-img.jpg',x = None, y = None, w = 0, h = 0, type = '', link = '')
            path = 'inspection.pdf'
            pieval =1
            subprocess.Popen([path], shell=True)
            cursor.close
            connection.close()
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, 'Message - Success', "Inspection completed successfully!!", QMessageBox.Ok, QMessageBox.Ok)
                   
        #cv2.imshow('image', img)
    def checkstatus(self):
        if self.textbox1.text() == '':
            print("Please enter Weight")
            QMessageBox.information(self, 'Message - Oops', "Please enter Weight!!", QMessageBox.Ok, QMessageBox.Ok)
            self.textbox1.setFocus()
            
        if self.texttkn.text() =='':
            QMessageBox.information(self, 'Message - Oops', "Token # cannot be empty!!", QMessageBox.Ok, QMessageBox.Ok)
            self.texttkn.setFocus()
    def initUI(self):
        pieval =0
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setStyleSheet("background-color: #C2E5D3;")
        self.label1 = QLabel('Select Location', self)
        self.label1.move(40, 110)
        self.label1.resize(200, 40)
        self.lblfarm = QLabel('Select Farmer', self)
        self.lblfarm.move(340, 110)
        self.lblfarm.resize(200, 40)
        self.label2 = QLabel('Tea Leaves Inspection', self)
        self.label2.move(200, 50)
        #self.label2 = QLabel('Times font', self)
        self.label2.setFont(QFont('Arial', 20,))
        self.label2.resize(800, 40)
        if pieval == 1:
            self.im = QPixmap("inspection.png")
            self.labelpie = QLabel(self)
            self.labelpie.move(1100,0)
            self.labelpie.resize(600,700)
            self.labelpie.setPixmap(self.im)
        else:
            self.labelpie = QLabel(self)
            self.labelpie.move(1100,0)
            self.labelpie.resize(600,600)
        
        
        if pieval == 1:
            self.im = QPixmap("graph.png")
            self.labelgraph = QLabel(self)
            self.labelgraph.move(400,0)
            self.labelgraph.resize(1000,900)
            self.labelgraph.setPixmap(self.im)
        else:
            self.labelgraph = QLabel(self)
            self.labelgraph.move(1500,0)
            self.labelgraph.resize(600,600)
            
        if pieval == 1:
            self.im = QPixmap("qr-img.jpg")
            self.labelqr = QLabel(self)
            self.labelqr.move(900,500)
            self.labelqr.resize(500,500)
            self.labelqr.setPixmap(self.im)
        else:
            self.labelqr = QLabel(self)
            self.labelqr.move(1200,500)
            self.labelqr.resize(400,400)
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(150, 170)
        self.textbox1.resize(80,20)
        self.textbox1.setValidator(QIntValidator())
        #self.textbox1.editingFinished.connect(self.checkstatus)
        self.lblunit = QLabel('KG', self)
        self.lblunit.move(250, 170)
        self.lblunit.resize(80, 20)
        self.lblwt = QLabel('Enter Weight', self)
        self.lblwt.move(40, 160)
        self.lblwt.resize(150, 40)
        
        self.labelcam = QLabel(self)
        self.labelcam.move(90, 240)
        self.labelcam.resize(1000, 450)
        self.imgLabel = QLabel('', self)
        self.imgLabel.move(20, 300)
        self.imgLabel.resize(950, 500)
        self.lblToken = QLabel('Token #:', self)
        self.lblToken.move(320, 170)
        self.lblToken.resize(80, 20)
        
        self.texttkn = QLineEdit(self)
        self.texttkn.move(400, 170)
        self.texttkn.resize(120,20)
        self.texttkn.setValidator(QIntValidator())
        
        self.radio1 = QRadioButton("M1 (High)", self)
        self.radio1.move (550,170)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.check)
        
        self.radio2 = QRadioButton("M2 (Low)", self)
        self.radio2.move (650,170)
        #self.radiobutton.setText = "B"
        self.radio2.clicked.connect(self.check)
        #self.texttkn.editingFinished.connect(self.checkstatus)
        '''
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        '''
        # Create a button in the window
        self.button = QPushButton('Process', self)
        self.button.move(400,220)
        self.button.clicked.connect(self.click_event)
        self.ExitButton = QPushButton('Exit',self)
        self.ExitButton.clicked.connect(sys.exit)
        self.ExitButton.move(550,220)
        '''
        self.btnsaveimg = QPushButton('Save Image', self)
        self.btnsaveimg.move(900,500)
        self.btnsaveimg.clicked.connect(self.save_image)
        '''
        self.btnsaveimg = QPushButton('Save Image', self)
        self.btnsaveimg.move(1000,500)
        self.btnsaveimg.clicked.connect(self.save_image)
        
        self.btndisplayimg = QPushButton('Display Image', self)
        self.btndisplayimg.move(1000,400)
        self.btndisplayimg.clicked.connect(self.OnClicked)
        self.combo_box1 = QComboBox(self)
        self.combo_box1.move(150, 120)
        self.combo_box1.resize(150,20)
       # location_list = ["Location1", "location2"]
        # making it editable
        self.combo_box1.setEditable(False)
       
        self.combo_box2 = QComboBox(self)
        # setting geometry of combo box
        self.combo_box2.move(450, 120)
        self.combo_box2.resize(250,20)
        #farmer_list = ["Farmer1", "Farmer2"]
        # making it editable
        self.combo_box2.setEditable(False)
        self.combo_box1.currentIndexChanged.connect(self.selectionchange)
       
        connection = mysql.connector.connect(user='root', password='Password123#$',
                          host='127.0.0.1',
                          database='tea_project')
        cursor = connection.cursor()
        sql_select_Query1 ="select location from location" 
        #sql_select_Query2 ="select farmername from farmers_detail" 
        #sql_select_Query = "insert into inspetion_detail values ("
        
        cursor.execute(sql_select_Query1)
        resultsloc = cursor.fetchall()
        #print(resultsloc)
        #self.combo_box1.addItem('')
        for i in resultsloc:
            self.combo_box1.addItem(str(i[0]))
        cursor.close
        #cursor = connection.cursor()
        #cursor.execute(sql_select_Query2)
        #resultsfarm = cursor.fetchall()
        #print(resultsfarm)
        #self.combo_box2.addItem('')
        #for i in resultsfarm:
            #self.combo_box2.addItem(str(i[0]))   
        #results_for_combobox = [result[0] for result in results]
        #cursor.close()
        connection.close()
        
        self.show()
        
    def OnClicked(self):
        import datetime
        #cap =cv2.VideoCapture(1,cv2.CAP_DSHOW)
        cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        while True:
            ret,frame =cap.read()
            if ret == True:
                self.display_image(frame,1)
                cv2.waitKey(1)
                if self.logic == 2:
                   #print ('hannah')
                   self.value = self.value+1
                   now1 = datetime.datetime.now()
                   now_str1 = now1.strftime("%Y-%m-%d-%H-%M-%S")
                   outfilename1 = 'Img-{}.jpg'.format(now_str1)
                   path = 'C:/hannah/demo/teaimages'
                   cv2.imwrite(os.path.join(path, outfilename1), frame)
                  # cv2.imwrite('c:/hannah/demo/teaimages/%s.jpg'%(self.value), frame)
                   self.logic = 1
                   QMessageBox.information(self, 'Message - Success', "Image saved!!", QMessageBox.Ok, QMessageBox.Ok)
                   break
            else:
                print("Return not found")
                break
        cap.release()
        cv2.destroyAllWindows() 
    def check(self):
        # checking if it is checked
        if self.radio1.isChecked():
            print("Max")
            Moist = 90
        else:
            print("Low")
            Moist = 73
    def display_image(self,img,winndow =1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img,img.shape[1],img.shape[0],qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    def save_image(self):
        self.logic = 2 
        
    def Run_Teach(self):
        if QApplication.instance():
            app = QApplication.instance()
        else:
            app = QApplication(sys.argv)
        
        self.run('cam.py')
       
        
    def save_rbg(self):
       
        list_of_files = glob.glob(r'C:\hannah\demo\teaimages\*.jpg') 
        latest_file = max(list_of_files, key=os.path.getctime)
        img = cv2.imread(latest_file, 1)    
        valr = 0
        valg = 0
        valb = 0
        ct =0
        now = datetime.now()
        today = date.today()
        current_time = now.strftime("%H.%M.%S")
        for i in range (0,50):
            x = random.randint(50,450)
            y = random.randint(70,400)
            #print(x, ' ', y)
            font = cv2.FONT_HERSHEY_SIMPLEX
     
            b = img[y, x, 0]
            g = img[y, x, 1]
            r = img[y, x, 2]
            #print (r,g,b)
            valr = valr +r
            valg = valg +g
            valb = valb +b
            ct = ct +1
        avgR = valr/ct
        avgG = valg/ct
        avgB = valb/ct
        '''
        combined = str(today) + ' ' + str(current_time) 
        connection = mysql.connector.connect(user='root', password='Password123#$',
                              host='127.0.0.1',
                                  database='tea_project')
        cursor = connection.cursor() 
        if self.radio1.isChecked():
            grade = self.radio1.text()
        elif self.radio2.isChecked():
            grade = self.radio2.text()
        elif self.radio3.isChecked():
            grade = self.radio3.text()
        sql_select_Query ="insert into ref_data (date,Grade,Red,Green,Blue) values (%s,%s,%s,%s,%s)"
        val = (combined,grade,avgR,avgG,avgB)
        cursor.execute(sql_select_Query,val)
        connection.commit()
        cursor.close
        connection.close()
        '''
        
    def run(self, path):
        subprocess.call(['python',path])
    def selectionchange(self): 
        #print("Hi")
        connection = mysql.connector.connect(user='root', password='Password123#$',
                          host='127.0.0.1',
                          database='tea_project')
        cursor = connection.cursor() 
        sql_select_Queryfarm ="select farmername,farmer_id from farmers_detail where location_id = (select location_id from location where location ='" + str(self.combo_box1.currentText()) + "' order by farmername asc)" 
        cursor = connection.cursor()
        cursor.execute(sql_select_Queryfarm)
        resultsfarm = cursor.fetchall()
        #print(resultsfarm)
        #self.combo_box2.addItem('')
        self.combo_box2.clear()
        for i in resultsfarm:
            #self.combo_box2.addItem(str(i[0]) + '-' + str(i[1])) 
             self.combo_box2.addItem(str(i[0]))
        #results_for_combobox = [result[0] for result in results]
        cursor.close()
        connection.close()
    def on_click(self):
        #textboxValue = self.textbox1.text()
        QMessageBox.information(self, 'Message - pythonspot', "Tea Leaves Inspected/Report generated successfully! ", QMessageBox.Ok, QMessageBox.Ok)
        #self.textbox1.setText("")
    def onActivated(self, text):

        self.combo_box1.setText(text)
        self.combo_box1.adjustSize()
        self.combo_box2.setText(text)
        self.combo_box2.adjustSize()
def getColorName(R,G,B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                cname = csv.loc[i,"color_name"]
        return cname   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
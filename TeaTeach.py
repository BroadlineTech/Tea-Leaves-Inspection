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
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
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
from cv2 import *
from threading import Thread
from queue import Queue
import numpy as np
import imutils
from PIL import Image
from tkinter import *
from PIL import Image, ImageTk
from cv2 import (VideoCapture, namedWindow, imshow, waitKey, destroyWindow, imwrite)
import serial
import csv
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    def run(self):
        log = 1
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            img_counter = 0
            if ret:
               
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(900, 700, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                if self.log == 2:
                   print (hannah)
                   self.value = self.value+1
                   cv2.imwrite('HANNAH.JPG', frame)
        cap.release
        cv2.destroyAllWindows()        
        
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Tea Leaves Teaching'
        self.setWindowIcon(QtGui.QIcon('tealeaf.jpg'))
        self.left = 75
        self.top = 75
        self.width = 1800
        self.height = 1000
        self.data = None
        self.logic =0
        self.value =1
        #cap = cv2.VideoCapture(0)
        self.initUI()
        
    def setImage(self, image):
        self.labelcam.setPixmap(QPixmap.fromImage(image))
    
    
    
    def checkstatus(self):
        if self.textbox1.text() == "":
            print("Please enter Weight")
            self.textbox1.setFocus()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
       
        self.labelcam = QLabel(self)
        self.labelcam.move(90, 100)
        self.labelcam.resize(1000, 400)
        #th = Thread(self)
        #th.changePixmap.connect(self.setImage)
        #th.start()
        self.label2 = QLabel('Tea Leaves Teaching', self)
        self.label2.move(200, 50)
        #self.label2 = QLabel('Times font', self)
        self.label2.setFont(QFont('Arial', 20,))
        self.label2.resize(800, 40)
        '''
        self.label3 = QLabel('', self)
        self.label3.move(20, 350)
        self.label3.resize(950, 300)
        self.label3.setStyleSheet("background-image : url(tea01.jpg);border:none;")
        '''
        self.imgLabel = QLabel('', self)
        self.imgLabel.move(20, 300)
        self.imgLabel.resize(950, 400)
        self.ExitButton = QPushButton('Exit',self)
        self.ExitButton.clicked.connect(sys.exit)
        self.ExitButton.move(650,190)
        '''
        self.btnteach = QPushButton('Teach', self)
        self.btnteach.move(620,190)
        self.btnteach.clicked.connect(self.Run_Teach)
        '''
        self.btnsave = QPushButton('Save', self)
        self.btnsave.move(500,190)
        self.btnsave.clicked.connect(self.save_rbg)
        
        self.btnsaveimg = QPushButton('Save Image', self)
        self.btnsaveimg.move(1000,500)
        self.btnsaveimg.clicked.connect(self.save_image)
        
        self.btndisplayimg = QPushButton('Display Image', self)
        self.btndisplayimg.move(1000,400)
        self.btndisplayimg.clicked.connect(self.OnClicked)
        
        self.label1 = QLabel('Select One', self)
        self.label1.move(160, 190)
        self.label1.resize(200, 40)
        self.combograde = QComboBox(self)
        # setting geometry of combo box
        self.combograde.move(250, 190)
        self.combograde.resize(200,30)
        self.combograde.addItem ("Teach A - 1")
        self.combograde.addItem ("Teach A - 2")
        self.combograde.addItem ("Teach A - 3")
        self.combograde.addItem ("Teach A - 4")
        self.combograde.addItem ("Teach A - 5")
        self.combograde.setEditable(False)
        self.radio1 = QRadioButton("Grade A", self)
        self.radio1.move (200,120)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.check)
        
        self.radio2 = QRadioButton("Grade B", self)
        self.radio2.move (280,120)
        #self.radiobutton.setText = "B"
        self.radio2.clicked.connect(self.check)
        
        self.radio3 = QRadioButton("Grade C", self)
        self.radio3.move (360,120)
        self.radio3.clicked.connect(self.check)
        self.radio4 = QRadioButton("Grade D", self)
        self.radio4.move (440,120)
        self.radio4.clicked.connect(self.check)
        self.lbllist = QLabel('Existing Standards (A-Finest,B-Fine,C-Good, D-Bad)', self)
        self.lbllist.setFont(QFont('Arial',12 ,))
        self.lbllist.move(890, 80)
        self.lbllist.resize(800, 40)
        self.listwidget = QListWidget(self)
        self.listwidget.move(950, 150)
        self.listwidget.resize(200,80)
        connection = mysql.connector.connect(user='root', password='Password123#$',
                          host='127.0.0.1',
                          database='tea_project')
        cursor = connection.cursor()
        cursor.execute ("select distinct grade,category from ref_data order by grade,category")
        i =0
        for x in cursor.fetchall():
            self.listwidget.addItem(str(x[0]) + '-' + str(x[1]))
            i =i+1
            
        cursor.close
        connection.close
        #self.ShowFeed()     

        #self.cameraLabel = Label(self, bg="white", borderwidth=10, relief="groove")
        '''
        connection = mysql.connector.connect(user='root', password='Password123#$',
                          host='127.0.0.1',
                          database='tea_project')
        cursor = connection.cursor()
        '''
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
        
    def check(self):
          
        # checking if it is checked
        if self.radio1.isChecked():
            #print(self.radio1.text())
            self.combograde.clear()
            self.combograde.addItem ("Teach A - 1")
            self.combograde.addItem ("Teach A - 2")
            self.combograde.addItem ("Teach A - 3")
            self.combograde.addItem ("Teach A - 4")
            self.combograde.addItem ("Teach A - 5")
            
        elif self.radio2.isChecked():
            #print(self.radio2.text())
            self.combograde.clear()
            self.combograde.addItem ("Teach B - 1")
            self.combograde.addItem ("Teach B - 2")
            self.combograde.addItem ("Teach B - 3")
            self.combograde.addItem ("Teach B - 4")
            self.combograde.addItem ("Teach B - 5")
        elif self.radio3.isChecked():
            #print(self.radio3.text())
            self.combograde.clear()
            self.combograde.addItem ("Teach C - 1")
            self.combograde.addItem ("Teach C - 2")
            self.combograde.addItem ("Teach C - 3")
            self.combograde.addItem ("Teach C - 4")
            self.combograde.addItem ("Teach C - 5")
        elif self.radio4.isChecked():
            #print(self.radio4.text())
            self.combograde.clear()            
            self.combograde.addItem ("Teach D - 1")
            self.combograde.addItem ("Teach D - 2")
            self.combograde.addItem ("Teach D - 3")
            self.combograde.addItem ("Teach D - 4")
            self.combograde.addItem ("Teach D - 5")
       
    def Run_Teach(self):
        if QApplication.instance():
            app = QApplication.instance()
        else:
            app = QApplication(sys.argv)
        
        self.run('cam.py')
    
    def save_rbg(self):
        import serial
        import csv
        Tsensor1 = ''
        Tsensor2 = ''
        Tsensor3 = ''
        Tsensor4 = ''
        Tsensor5 = ''
        ret = QMessageBox.question(self, 'MessageBox', "Has the image been saved?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            return
        else:
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
            try:
                ser = serial.Serial('com6',9600)
                ser.flushInput()
                for i in range (1,20):
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
                        
                        '''
                        if (decoded_bytes.find("Humidity") != -1):
                            if (humidity == ''):
                                humidity  = decoded_bytes[-10:]
                                humidity =humidity.strip()
                                print(humidity)
                        
                        elif (decoded_bytes.find("Celsius") != -1):
                            if (tempc == ''):
                                tempc = decoded_bytes[-8:]
                                tempc = tempc.strip()
                                print(tempc)
                            
                        elif (decoded_bytes.find("Fahrenheit") != -1):
                            if (tempfar == ''):
                                tempfar = decoded_bytes[-8:]
                                tempfar = tempfar.strip()
                                print(tempfar)
                        
                        elif (decoded_bytes.find("average persentage") != -1):
                            if (capacitance == ''):
                                capacitance = decoded_bytes[-8:]
                                capacitance= capacitance.strip()
                                print(capacitance)
                        '''
                        if (decoded_bytes.find("1st sensor") != -1):
                            if (Tsensor1 == ''):
                                Tsensor1 = decoded_bytes[-7:]
                                Tsensor1= Tsensor1.strip()
                                #print(Tsensor1)
                        elif (decoded_bytes.find("2nd sensor") != -1):
                            if (Tsensor2 == ''):
                                Tsensor2 = decoded_bytes[-7:]
                                Tsensor2= Tsensor2.strip()
                                #print(Tsensor2)
                        elif (decoded_bytes.find("3rd sensor") != -1):
                            if (Tsensor3 == ''):
                                Tsensor3 = decoded_bytes[-7:]
                                Tsensor3= Tsensor3.strip()
                                #print(Tsensor3)
                        elif (decoded_bytes.find("4th sensor") != -1):
                            if (Tsensor4 == ''):
                                Tsensor4 = decoded_bytes[-7:]
                                Tsensor4= Tsensor4.strip()
                                #print(Tsensor4)
                        elif (decoded_bytes.find("5th sensor") != -1):
                            if (Tsensor5 == ''):
                                Tsensor5 = decoded_bytes[-7:]
                                Tsensor5= Tsensor5.strip()
                                #print(Tsensor5)
                                
                    #print(Tsensor4,Tsensor5)
                    if Tsensor4 == '':
                        Tsensor4 =0
                    if Tsensor5 == '':
                        Tsensor5 =0
            
            except serial.SerialException as e:
                
                Tsensor1 =0
                Tsensor2 =0
                Tsensor3 =0
                Tsensor4 =0
                Tsensor5 =0
        #print (Tsensor1,Tsensor2,Tsensor3)    
        for i in range (0,100):
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
        elif self.radio4.isChecked():
            grade = self.radio4.text()
        category = self.combograde.currentText()[-1]
        #print (category)
        cursor.execute("select * from ref_data where grade ='" + grade + "' and category =" + category )
        row = cursor.fetchone()
        if row is None:
            sql_update_query = "select max(ref_id) as ref_id from ref_data"
            cursor.execute (sql_update_query)
            for x in cursor.fetchall():
                if x[0] is None:
                    refid = 1
                else:
                    refid = x[0] +1
            sql_select_Query ="insert into ref_data (ref_id,date,Grade,category,Red,Green,Blue,Tsensor1,Tsensor2,Tsensor3,Tsensor4,Tsensor5) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (refid,combined,grade,category,avgR,avgG,avgB,Tsensor1,Tsensor2,Tsensor3,Tsensor4,Tsensor5)
            cursor.execute(sql_select_Query,val)
            connection.commit()
            
            
        else:
            print (Tsensor1,Tsensor2,Tsensor3,grade,category)
            #sql_update_query = """update ref_data set Red = %s and Green = %s and Blue = %s where grade = %s and category = %s"""
            sql_update_query = "update ref_data set Red = %s , Green = %s , Blue = %s , Tsensor1 = %s , Tsensor2 = %s , Tsensor3 = %s , Tsensor4 = %s , Tsensor5 = %s where grade = %s and category = %s"
            #sql_update_query = "update ref_data set Red =" + str(avgR)  + " and Green =" + str(avgG) + " and Blue =" + str(avgB) + " and Tsensor1=" + str(Tsensor1) + " where grade ='" + str(grade) + "' and category =" + str(category)  
            val = (avgR,avgG,avgB,Tsensor1,Tsensor2,Tsensor3,Tsensor4,Tsensor5,grade,category)
            cursor.execute(sql_update_query,val)
            connection.commit()
        cursor.execute ("select distinct grade,category from ref_data order by grade,category")
        i =0
        self.listwidget.clear()
        for x in cursor.fetchall():
            
            self.listwidget.addItem(str(x[0]) + '-' + str(x[1]))
            i =i+1
        cursor.close
        connection.close()
        QMessageBox.information(self, 'Message - Success', "Tea Leaves " + grade + "-" + category + " has been added/updated1 successfully! ", QMessageBox.Ok, QMessageBox.Ok)
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
        QMessageBox.information(self, 'Message - pythonspot', "Tea Leaves been inspected successfully! ", QMessageBox.Ok, QMessageBox.Ok)
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
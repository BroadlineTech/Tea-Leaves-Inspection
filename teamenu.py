import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import PyQt5.QtGui     as Gui
import PyQt5.QtWidgets as Wid
import PyQt5.QtCore    as Cor 
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Tea Leaves Inspection'
        self.setWindowIcon(QtGui.QIcon('tea-background.jpg'))
        self.setStyleSheet("background-image: url(tea-background.jpg); background-attachment: fixed")
        self.initUI()
        

    def initUI(self):
        
        mainMenu = self.menuBar()
        mainMenu.setFont(QFont('Times', 13))
        pyGuiMenu = mainMenu.addMenu('&Teach')
        NewMenu = pyGuiMenu.addAction('&New')
        NewMenu.setFont(QFont('Times', 12))
        NewMenu.triggered.connect(self.teachwindow)
        #prevMenu.setShortcut("Ctrl+N")
        pyGuiMenu = mainMenu.addMenu('Inspect')
        
        #prevMenu = pyGuiMenu.addMenu('Preview')
        
        subItemTable = Wid.QAction('New', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.triggered.connect(self.newWindow)
        subItemTable = Wid.QAction('New', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("New Window")
        
        subItemTable.triggered.connect(self.newWindow)     # +++

        pyGuiMenu.addAction(subItemTable) 
        pyGuiMenu.setFont(QFont('Times', 12))
        subItemExit = Wid.QAction('Exit', self)
        '''
        subItemExit.setShortcut("Ctrl+E")
        subItemExit.setStatusTip("Exit Application")
        subItemExit.triggered.connect(self.close_App)
        
        pyGuiMenu.addAction(subItemExit);
        '''
        pyGuiMenu = mainMenu.addMenu('Exit Application')
        #pyGuiMenu.triggered.connect(self.close_App)
        pyGuiMenu.triggered.connect(self.close_App)
        pyGuiMenu.addAction(subItemExit);
        pyGuiMenu.setFont(QFont('Times', 12))
        #Teach.triggered.connect(lambda: self.OpenTeachWindow())
        '''
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
        
        exitButton = mainMenu.addMenu('Exit')
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        '''
        self.setGeometry(10, 10, 2200, 1500)
        self.setWindowTitle('Tea Leaves Inspection')
        self.show()
    def close_App(self):
        reply = Wid.QMessageBox.question(
            self, 
            "Exit Application", 
            "Are you sure to close the window?", 
            Wid.QMessageBox.Yes | Wid.QMessageBox.No, 
            Wid.QMessageBox.No
        )
        if reply == Wid.QMessageBox.Yes:
           sys.exit()
    def newWindow(self):                                    # +++
        
        self.run('TeaMain.py')
    def teachwindow(self):                                    # +++
        
        self.run('TeaTeach.py')
    def OpenTeachWindow(self):
        if QApplication.instance():
            app = QApplication.instance()
        else:
            app = QApplication(sys.argv)
        app.exec_()
        self.run('TeaMain.py')
        #w = QDialog(self)
        #w.resize(640, 480)
        #w.exec_()
    def run(self, path):
        subprocess.call(['python',path])
def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()
import sys
import os
from math import sqrt
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMenuBar, QAction, qApp, QDialog, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("calc2.ui", self)
        
        rec = QApplication.desktop()
        rec = rec.screenGeometry()
        width = rec.width()
        height = rec.height()
        
        self.setLayout(self.verL)
        
        self.le.setMaximumSize(1000 * width / 1920, 95 * height / 1080)
        
        self.nums = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,
                     self.btn6, self.btn7, self.btn8, self.btn9, self.btn0]
        
        self.operators = [self.btnplus, self.btnminus, self.btnmul, self.btndiv]
        
        for btn in self.nums:
            btn.clicked.connect(self.numToBuffer)
            
        for op in self.operators:
            op.clicked.connect(self.opToBuffer)
            
        self.btnc.clicked.connect(self.clear)
        self.btnwipe.clicked.connect(self.clearSign)
        self.btndot.clicked.connect(self.addDot)
        self.btneq.clicked.connect(self.evalBuffer)
        self.btnsqr.clicked.connect(self.squareBuffer)
        self.btnsqrt.clicked.connect(self.squareRootBuffer)
        self.btnrev.clicked.connect(self.reverseBuffer)
        self.btnpm.clicked.connect(self.changeSign)
        
        self.canPutDot = True
        self.canDoubleOper = False
        
        self.doubleOper = ''
        
    def numToBuffer(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text() == "Error!" or self.le.text() == "inf":
            self.clear()
        self.le.setText(self.le.text() + self.sender().text())  
        
    def opToBuffer(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text():
            if all([self.le.text()[-1] != s for s in ['+', '-', '/', '*', '.', '!']]):
                self.le.setText(self.le.text() + self.sender().text())
                self.canPutDot = True
        
    def clear(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        self.le.setText("")
        
    def clearSign(self):
        if self.le.text() == "Error!" or self.le.text() == "inf":
            self.clear()
            return None
        if self.le.text():
            if self.le.text()[-1] in ['+', '-', '/', '*']:
                self.canPutDot = False
            self.le.setText(self.le.text()[:-1])
        
        
    def addDot(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text():
            if (self.le.text()[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] and 
                ('.' not in self.le.text() or self.canPutDot)):
                    self.le.setText(self.le.text() + '.')
                    self.canPutDot = False
                    
    def evalBuffer(self):
        if not self.le.text() or self.le.text() == "Error!" or self.le.text() == "inf":
            return None
        
        try:
            additional = ''
                
            if ((self.le.text()[-1] in ['+', '-', '*', '/']) and
                (all([(s not in str(self.le.text())[:-1] or (self.le.text().count('-') == 1 and self.le.text()[0]=='-') or (s == '+' or s == '-') and (self.le.text()[self.le.text().find(s)-1]=='e')) for s in ['+', '-', '*', '/']]))):
                    additional = self.le.text()[:-1]
                    
            self.le.setText(self.le.text() + additional)
            
            if self.canDoubleOper:
                self.le.setText(self.le.text() + self.doubleOper)
                
            else:
                if self.le.text():
                    indexesOfOperators = ([i for i in range(len(self.le.text())) if self.le.text()[i] in ['+', '-', '*', '/']])
                    
                    if indexesOfOperators:
                        indexOfOperator = indexesOfOperators[-1]
                        
                        if len(indexesOfOperators) >= 2:
                            indexOfOperator = indexesOfOperators[[i for i in range(len(indexesOfOperators)) if self.le.text()[indexesOfOperators[i]] in ["+", "-"]][-1]] 
                        
                        self.doubleOper = self.le.text()[(indexOfOperator):]
                        self.canDoubleOper = True
            
            res = eval(self.le.text())
            
            if float(res).is_integer() and 'e' not in str(res):
                res = int(res)
                
        except Exception:
            self.le.setText("Error!")
            return None
        
        if len(str(res)) > 13 and '.' in str(res):
            if (str(res))[-11:-2] == '000000000' or (str(res))[-11:-2] == '999999999':
                res = round(res, len(str(res)[str(res).find('.'):-14]))
        
        self.le.setText(str(res))
        
    def squareBuffer(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text() and not self.le.text() == "Error!" and not self.le.text() == "inf":
            self.evalBuffer()
            
            try:
                res = float(self.le.text()) ** 2
            except Exception:
                self.le.setText("Error!")
                return None
                
            if float(res).is_integer() and 'e' not in str(res):
                    res = int(res)  
                
            self.le.setText(str(res))
            
    def squareRootBuffer(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text() and not self.le.text() == "Error!" and not self.le.text() == "inf":
            self.evalBuffer()
            
            try:
                res = sqrt(float(self.le.text()))
            except Exception:
                self.le.setText("Error!")
                return None
                
            if float(res).is_integer() and 'e' not in str(res):
                    res = int(res)  
                
            self.le.setText(str(res))
            
    def reverseBuffer(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text() and not self.le.text() == "Error!" and not self.le.text() == "inf":
            self.evalBuffer()
            
            try:
                res = 1 / (float(self.le.text()))
            except Exception:
                self.le.setText("Error!")
                return None
                
            if float(res).is_integer() and 'e' not in str(res):
                    res = int(res)  
                
            self.le.setText(str(res))
            
    def changeSign(self):
        self.canDoubleOper = False
        self.doubleOper = ''
        if self.le.text() and not self.le.text() == "Error!" and not self.le.text() == "inf":
            self.evalBuffer()
            
            try:
                res = 0 - float(self.le.text())
            except Exception:
                self.le.setText("Error!")
                return None
                
            if float(res).is_integer() and 'e' not in str(res):
                    res = int(res)  
                
            self.le.setText(str(res))
        

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.rec = QApplication.desktop()
        self.rec = self.rec.screenGeometry()
        self.w = self.rec.width()
        self.h = self.rec.height()
        
        self.initUI()
        
    def initUI(self):
        exitAct = QAction("&Exit", self)
        exitAct.triggered.connect(qApp.quit)
        exitAct.setShortcut("Ctrl+Q")
        
        aboutAct = QAction("&About", self)
        aboutAct.triggered.connect(self.showInfo)
        
        menubar = QMenuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(exitAct)
    
        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(aboutAct)
        
        self.setMenuBar(menubar)

        with open('menuStyle.css', 'r') as f:
            menubar.setStyleSheet(f.read())

        win = MainUI()
        self.setCentralWidget(win)
        
        self.resize(420 * self.w / 1920, 400 * self.h / 1080)
        
        self.setMaximumSize(894  * self.w / 1920, 730  * self.h / 1080)
        
        with open('generalStyle.css', 'r') as f:
            self.setStyleSheet(f.read())
        
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon(os.path.join("Resources", "calc.png")))
        self.show()
        
    def showInfo(self):
        win = AboutWindow()
        win.setWindowFlags(Qt.Widget)
        win.exec_()
        
class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.rec = QApplication.desktop()
        self.rec = self.rec.screenGeometry()
        self.w = self.rec.width()
        self.h = self.rec.height()

        if sys.platform == 'linux':
            font = QFont("Liberation Serif")
        else:
            font = QFont("Calibri")
        
        self.lbl = QLabel("Calculator\nVersion 0.9\n\n©Nikita Morozov 2016", self)
        self.lbl.move(10 * self.w / 1920, 15 * self.h / 1080)
        font.setPixelSize(26)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: lightgray")
    
        self.setStyleSheet("QDialog {background-color: #3D3D3D; }")
        
        self.setFixedSize(300 * self.w / 1920, 190 * self.h / 1080)
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon(os.path.join("Resources", "calc.png")))
        self.show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main()
    sys.exit(app.exec_())
    
    

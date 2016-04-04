#!/usr/bin/python

import sys, rospy
from PyQt4 import QtGui, QtCore
from geometry_msgs.msg import Twist
from std_msgs.msg import ColorRGBA, Float32, Bool

class LEDWidget(QtGui.QLabel):
   
    def __init__(self, size, rgb):
        super(QtGui.QLabel, self).__init__()
        pixmap = QtGui.QPixmap(size[0], size[1])
        self.setPixmap(pixmap)
        self.rgb = rgb
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Base)

    def setRGB(self, r, g, b):
        self.rgb = [r,g,b]
        p = QtGui.QPalette()
        p.setColor(self.backgroundRole(), QtGui.QColor(self.rgb[0], self.rgb[1], self.rgb[2]))
        self.setPalette(p)
        self.update()
  
    def paintEvent(self, e):
        super(QtGui.QLabel, self).paintEvent(e)
        #qp = QtGui.QPainter()
        #qp.begin(self)
        #qp.end()         

class LEDConfig(QtGui.QWidget):

    def __init__(self, parentWindow):
        super(QtGui.QWidget, self).__init__()
        self.parentWindow = parentWindow
        self.initUI()
        self.hide()
    
    def initUI(self):   

        self.r_label = QtGui.QLabel("R")
        self.r_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.r_sl.setMinimum(0)
        self.r_sl.setMaximum(255)
        self.r_sl.setValue(self.parentWindow.ledRVal)
        self.r_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.r_sl.setTickInterval(1)
        self.r_sl.valueChanged.connect(self.valuechange)

        self.g_label = QtGui.QLabel("G")
        self.g_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.g_sl.setMinimum(0)
        self.g_sl.setMaximum(255)
        self.g_sl.setValue(self.parentWindow.ledGVal)
        self.g_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.g_sl.setTickInterval(1)
        self.g_sl.valueChanged.connect(self.valuechange)

        self.b_label = QtGui.QLabel("B")
        self.b_sl = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.b_sl.setMinimum(0)
        self.b_sl.setMaximum(255)
        self.b_sl.setValue(self.parentWindow.ledBVal)
        self.b_sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.b_sl.setTickInterval(1)
        self.b_sl.valueChanged.connect(self.valuechange)

        self.led = LEDWidget([20,20],
                             [self.parentWindow.ledRVal,
                              self.parentWindow.ledGVal,
                              self.parentWindow.ledBVal])
        
        self.btnOK = QtGui.QPushButton("OK")
        self.btnCancel = QtGui.QPushButton("Cancel")
        self.btnOK.clicked.connect(self.update)
        self.btnCancel.clicked.connect(self.cancel)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.led)
        r_layout = QtGui.QHBoxLayout()
        r_layout.addWidget(self.r_label)
        r_layout.addWidget(self.r_sl)
        layout.addLayout(r_layout)
        g_layout = QtGui.QHBoxLayout()
        g_layout.addWidget(self.g_label)
        g_layout.addWidget(self.g_sl)
        layout.addLayout(g_layout)
        b_layout = QtGui.QHBoxLayout()
        b_layout.addWidget(self.b_label)
        b_layout.addWidget(self.b_sl)
        layout.addLayout(b_layout)
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.addWidget(self.btnOK)
        btn_layout.addWidget(self.btnCancel)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.show()

    def update(self):
        
        self.parentWindow.ledRVal = self.r_sl.value()
        self.parentWindow.ledGVal = self.g_sl.value()
        self.parentWindow.ledBVal = self.b_sl.value()        
        self.parentWindow.setLED(self.parentWindow.ledRVal,
                                 self.parentWindow.ledGVal,
                                 self.parentWindow.ledBVal)
        self.led.setRGB(self.parentWindow.ledRVal,
                        self.parentWindow.ledGVal,
                        self.parentWindow.ledBVal)
        self.hide()
        
    def cancel(self):
        self.r_sl.setValue(self.parentWindow.ledRVal)
        self.g_sl.setValue(self.parentWindow.ledGVal)
        self.b_sl.setValue(self.parentWindow.ledBVal)
        self.hide()

    def valuechange(self):
        self.led.setRGB(self.r_sl.value(),
                        self.g_sl.value(),
                        self.b_sl.value())
        self.led.update()

class SpheroDashboardForm(QtGui.QMainWindow):
    
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()
        self.resize(600, 480)
        
        self.ledRVal = 255
        self.ledGVal = 255
        self.ledBVal = 255
        self.ledConfig = LEDConfig(self)
        
        self.initUI()

        rospy.init_node('sphero_dashboard', anonymous=True)
        self.cmdVelPub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.cmdVelSub = rospy.Subscriber("cmd_vel", Twist, self.cmdVelCallback)
      
        self.ledPub = rospy.Publisher('set_color', ColorRGBA, queue_size=1)

        
    def initUI(self):
        
        ledAction = QtGui.QAction('LED', self)
        ledAction.triggered.connect(self.showLedConfig)
        
        menubar = self.menuBar()
        ledMenu = menubar.addMenu('&LED')
        ledMenu.addAction(ledAction)        

        self.cmdVelLabel = QtGui.QLabel("cmd_vel")
        self.cmdVelTextbox = QtGui.QTextEdit()
        self.cmdVelTextbox.setReadOnly(True)        

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.cmdVelLabel)
        layout.addWidget(self.cmdVelTextbox)
        self.setLayout(layout)
        self.setWindowTitle("Sphero dashboard")

        self.show()

    def showLedConfig(self):
        self.ledConfig.show()     

    def setLED(self, r, g, b):
        pass   

    def handleCmdVelMsg(self, text, stdout):
        self.cmdVelTextbox.moveCursor(QtGui.QTextCursor.End)
        self.cmdVelTextbox.ensureCursorVisible()
        self.cmdVelTextbox.insertPlainText(text)

    def cmdVelCallback(self, msg):
        pass

        
    def keyPressEvent(self, e):        
        if e.key() == QtCore.Qt.Key_Left:
            print "letf"

        elif e.key() == QtCore.Qt.Key_Right:
            print "right"   
        
        elif e.key() == QtCore.Qt.Key_Up:
            print "up"
 
        elif e.key() == QtCore.Qt.Key_Down:
            print "down"

        

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    w = SpheroDashboardForm()
    sys.exit(app.exec_())
  
        

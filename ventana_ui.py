# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1495, 900)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("background-color : #222831")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 55, 1461, 831))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(QtGui.QFont('Consolas', 11))
        self.plainTextEdit.setStyleSheet("color : #EEEEEE;background-color: #393E46;border: 1px solid white;")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plainTextEdit_2.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_2.setFont(QtGui.QFont('Consolas', 11))
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setStyleSheet("color : #EEEEEE;background-color: #393E46;border: 1px solid white;")
        self.horizontalLayout.addWidget(self.plainTextEdit_2)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 0, 1461, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_1 = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.setStyleSheet("background-color :rgb(201, 209, 217)")
        self.horizontalLayout_2.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("background-color :rgb(201, 209, 217)")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label.setStyleSheet("color:white")
        self.horizontalLayout_3.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setStyleSheet("background-color : rgb(201, 209, 217);")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("background-color :rgb(201, 209, 217)")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1098, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionCargar_Archivo = QtWidgets.QAction(MainWindow)
        self.actionCargar_Archivo.setObjectName("actionCargar_Archivo")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Proyecto 2 - 202010055"))
        self.pushButton_1.setText(_translate("MainWindow", "Abrir"))
        self.pushButton_2.setText(_translate("MainWindow", "Analizar"))
        self.label.setText(_translate("MainWindow", "Reportes"))
        self.pushButton_3.setText(_translate("MainWindow", "Generar"))
        self.actionCargar_Archivo.setText(_translate("MainWindow", "Cargar Archivo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
import tkinter as tk
from analizador_lexico import * 
from analizador_sintactico import * 
import os.path
from tkinter.filedialog import askopenfilename
import PyQt5
from ventana_ui import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.contenido = ""
        self.pushButton_1.clicked.connect(self.abrir)
        self.pushButton_2.clicked.connect(self.analizar)

    def abrir(self):
        archivo = open("entrada(1).lfp", 'r')
        self.contenido = archivo.read()
        archivo.close()
        self.plainTextEdit.setPlainText(self.contenido)

    def analizar(self): 
        texto = self.plainTextEdit.toPlainText()
        scanner = AnalizadorLexico()
        listas = scanner.analizar(texto)
        
        parser = AnalizadorSintactico(listas[0], listas[2])
        consola = parser.analizar()
        self.plainTextEdit_2.setPlainText(consola)
    
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


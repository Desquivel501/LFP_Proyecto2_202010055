import tkinter as tk
from analizador_lexico import * 
from analizador_sintactico import * 
from reportes import *
import os.path
from tkinter.filedialog import askopenfilename
import PyQt5
from ventana_ui import *
import copy

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.contenido = ""
        self.listaErrores = []
        self.listaTokens = []
        self.arbol = None
        lista = ["Reporte de Tokens","Reporte de Errores", "Árbol de derivación" ]
        self.comboBox.clear()
        self.comboBox.addItems(lista)
        self.pushButton_1.clicked.connect(self.abrir)
        self.pushButton_2.clicked.connect(self.analizar)
        self.pushButton_3.clicked.connect(self.generarReporte)

    def abrir(self):
        filename = askopenfilename()
        archivo = open(filename, 'r')
        self.contenido = archivo.read()
        archivo.close()
        self.plainTextEdit.setPlainText(self.contenido)

    def analizar(self): 
        texto = self.plainTextEdit.toPlainText()
        scanner = AnalizadorLexico()
        listas = scanner.analizar(texto)
        
        parser = AnalizadorSintactico(listas[0], listas[1])
        self.listaTokens = copy.deepcopy(listas[0])
        
        consola = parser.analizar()
        self.plainTextEdit_2.setPlainText(consola[0])
        self.listaErrores = consola[1]
        self.arbol = consola[2]
    
    def generarReporte(self):
        reportes = Reportes()
        current = str(self.comboBox.currentText())

        if current == "Reporte de Tokens":
            reportes.reporteTokens(reversed(self.listaTokens))
        elif current == "Reporte de Errores":
            reportes.reporteErrores(self.listaErrores)
        elif current == "Árbol de derivación":
            self.arbol.view()

    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


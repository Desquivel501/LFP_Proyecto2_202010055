import tkinter as tk
from analizador_lexico import * 
from analizador_sintactico import * 
import os.path
from tkinter.filedialog import askopenfilename

def leer(): 
    # filename = askopenfilename()
    archivo = open("prueba.txt", 'r')
    contenido = archivo.read()
    archivo.close()
    
    scanner = AnalizadorLexico()
    listas = scanner.analizar(contenido)
    scanner.impTokens()
    scanner.impErrores()
    
    parser = AnalizadorSintactico(listas[0])
    parser.analizar()
    
    
    
if __name__ == '__main__':
    leer()
    

from prettytable import PrettyTable
from functions import Functions
from reportes import Reportes

from graphviz import Digraph
import uuid

class AnalizadorSintactico:

    def __init__(self,tokens = [], errores=[]):
        self.errores = errores
        self.tokens = tokens
        self.tokens.reverse()
        self.reservadas = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR", "PUNTOCOMA"]
        self.lista = []
        self.claves = []
        self.funcion = Functions()
        self.reporte = Reportes()
        self.stream = ""
        self.g = Digraph('Arbol',format='png')
        self.inicio = ""

    def agregarError(self,obtenido,esperado,fila,columna):
        self.errores.append(
            "<ERROR SINTACTICO> Se obtuvo {}, se esperaba {}. Fila: {}, Columna: {}".format(
                obtenido,
                esperado,
                fila,
                columna
            )
        )
        tmp = self.tokens.pop()
        while tmp.tipo.upper() not in self.reservadas:
            tmp = self.tokens.pop()


    def impErrores(self):
        x = PrettyTable()
        x.field_names = ["Errores"]
        if len(self.errores)==0:
            print('No hay errores')
        else:
            for i in self.errores:
                x.add_row([i])
            self.stream += "\n" + str(x)
            # print(x)


    def impTabla(self):
        x = PrettyTable()
        x.field_names = self.claves
        if len(self.lista)==0:
            print('No hay Valores')
        else:
            for i in self.lista:
                x.add_row(i)
            self.stream += "\n" + str(x)

    def analizar(self):
        self.INICIO()
        self.impErrores()
        return (self.stream, self.errores, self.g)


    def INICIO(self):
        self.inicio = self.crearNodo('INICIO')
        self.INSTRUCCIONES(self.inicio)
        # self.g.view()

    def INSTRUCCIONES(self, nodoInicio):
        instrucciones = self.crearNodo('INSTRUCCIONES')
        self.agregarHijo(nodoInicio, instrucciones)
        self.inicio = instrucciones
        
        self.INSTRUCCION(nodoInicio)
        self.INSTRUCCIONES2(nodoInicio)

    def INSTRUCCIONES2(self, nodoInicio):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo.upper() in self.reservadas:
                self.INSTRUCCION(nodoInicio)
                self.INSTRUCCIONES2(nodoInicio)
            else:
                print("here1")
                self.agregarError(tmp.tipo,"Instruccion",tmp.linea,tmp.columna)
                self.INSTRUCCION(nodoInicio)
                self.INSTRUCCIONES2(nodoInicio)

        except IndexError:
            pass
        except Exception as e:
            print(e)
            pass

    def INSTRUCCION(self, nodoInicio):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo == 'imprimir':
                instruccion = self.crearNodo('INSTRUCCION')
                self.IMPRIMIR(nodoInicio, instruccion)
            elif tmp.tipo == 'imprimirln':
                instruccion = self.crearNodo('INSTRUCCION')
                self.IMPRIMIRLN(nodoInicio, instruccion)
            elif tmp.tipo == 'Claves':
                # instruccion = self.crearNodo('INSTRUCCION')
                self.CLAVES(nodoInicio, None)
            elif tmp.tipo == 'Registros':
                # instruccion = self.crearNodo('INSTRUCCION')
                self.REGISTROS(nodoInicio, None)
            elif tmp.tipo == 'conteo':
                instruccion = self.crearNodo('INSTRUCCION')
                self.CONTEO(nodoInicio, instruccion)
            elif tmp.tipo == 'promedio':
                instruccion = self.crearNodo('INSTRUCCION')
                self.PROMEDIO(nodoInicio, instruccion)
            elif tmp.tipo == 'contarsi':
                instruccion = self.crearNodo('INSTRUCCION')
                self.CONTARSI(nodoInicio, instruccion)
            elif tmp.tipo == 'datos':
                instruccion = self.crearNodo('INSTRUCCION')
                self.DATOS(nodoInicio, instruccion)
            elif tmp.tipo == 'sumar':
                instruccion = self.crearNodo('INSTRUCCION')
                self.SUMAR(nodoInicio, instruccion)
            elif tmp.tipo == 'max':
                instruccion = self.crearNodo('INSTRUCCION')
                self.MAX(nodoInicio, instruccion)
            elif tmp.tipo == 'min':
                instruccion = self.crearNodo('INSTRUCCION')
                self.MIN(nodoInicio, instruccion)
            elif tmp.tipo == 'exportarReporte':
                instruccion = self.crearNodo('INSTRUCCION')
                self.REPORTE(nodoInicio, instruccion)
            else:
                pass
            return instruccion
        except IndexError:
            pass
        except Exception as e:
            print(e)
            pass

    def IMPRIMIR(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimir":
            n0 = self.crearNodo('IMPRIMIR')
            n10 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n10)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n1 = self.crearNodo('ParentesisIzquierdo')
                n2 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n1, n2)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    cadena = cadena.replace('"', '')
                    self.stream += cadena
                    n3 = self.crearNodo('Cadena')
                    n4 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n3, n4)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n5 = self.crearNodo('ParentesisDerecho')
                        n6 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n5, n6)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            n7 = self.crearNodo('PuntoComa')
                            n8 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n7, n8)
                            
                            n9 = self.crearNodo('INSTRUCCION_IMPRIMIR')
                            self.agregarHijo(n9, n0)
                            self.agregarHijo(n9, n1)
                            self.agregarHijo(n9, n3)
                            self.agregarHijo(n9, n5)
                            self.agregarHijo(n9, n7)
                            
                            self.agregarHijo(self.inicio, nodoInstruccion)
                            self.agregarHijo(nodoInstruccion, n9)
                            self.inicio = nodoInstruccion

                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"IMPRIMIR",tmp.linea,tmp.columna)

    def IMPRIMIRLN(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimirln":
            n0 = self.crearNodo('IMPRIMIRLN')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n2)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n3 = self.crearNodo('ParentesisIzquierdo')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3, n4)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    cadena = cadena.replace('"', '')
                    self.stream += "\n" + cadena
                    n5 = self.crearNodo('Cadena')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5, n6)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n7 = self.crearNodo('ParentesisDerecho')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7, n8)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            n9 = self.crearNodo('PuntoComa')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9, n10)
                            
                            n11 = self.crearNodo('INSTRUCCION_IMPRIMIR')
                            self.agregarHijo(n11, n0)
                            self.agregarHijo(n11, n3)
                            self.agregarHijo(n11, n5)
                            self.agregarHijo(n11, n7)
                            self.agregarHijo(n11, n9)
                            
                            self.agregarHijo(self.inicio, nodoInstruccion)
                            self.agregarHijo(nodoInstruccion, n11)
                            self.inicio = nodoInstruccion
    
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"IMPRIMIRLN",tmp.linea,tmp.columna)

    def CLAVES(self, nodoInicio, nodoInstruccion):
        temp_row = []
        tmp = self.tokens.pop()
        if tmp.tipo == "Claves":
            tmp = self.tokens.pop()
            if tmp.tipo == "Igual":
                tmp = self.tokens.pop()
                if tmp.tipo == "CorcheteIzquierdo":
                    finish = False
                    while finish is False:
                        tmp = self.tokens.pop()
                        if tmp.tipo == "Cadena":
                            cadena = tmp.lexema
                            cadena = cadena.replace('"', '')
                            temp_row.append(cadena)

                            tmp = self.tokens.pop()
                            if tmp.tipo == "Coma":
                                continue
                            elif tmp.tipo == "CorcheteDerecho":
                                finish = True
                            else:
                                self.agregarError(tmp.tipo,"PuntoComa o CorcheteDerecho",tmp.linea,tmp.columna)
                        else:
                            self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
                            break
                else:
                    self.agregarError(tmp.tipo,"CorcheteIzquierdo",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"Igual",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"CLAVES",tmp.linea,tmp.columna)

        self.claves = temp_row

    def REGISTROS(self, nodoInicio, nodoInstruccion):

        tmp = self.tokens.pop()
        if tmp.tipo == "Registros":
            tmp = self.tokens.pop()
            if tmp.tipo == "Igual":
                tmp = self.tokens.pop()
                if tmp.tipo == "CorcheteIzquierdo":
                    registros = True
                    while registros:
                        tmp = self.tokens.pop()
                        if tmp.tipo == "LlaveIzquierda":
                            temp_row = []
                            finish = False
                            while finish is False:
                                tmp = self.tokens.pop()
                                if tmp.tipo == "Cadena" or tmp.tipo == "Decimal" or tmp.tipo == "Entero":
                                    cadena = tmp.lexema
                                    cadena = cadena.replace('"', '')
                                    temp_row.append(cadena)

                                    tmp = self.tokens.pop()
                                    if tmp.tipo == "Coma":
                                        continue
                                    elif tmp.tipo == "LlaveDerecha":
                                        finish = True
                                    else:
                                        self.agregarError(tmp.tipo,"PuntoComa o LlaveDerecha",tmp.linea,tmp.columna)
                                        break
                                else:
                                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
                                    break
                            self.lista.append(temp_row)

                        elif tmp.tipo == "CorcheteDerecho":
                            break
                        else:
                            self.agregarError(tmp.tipo,"LlaveIzquierda o CorcheteDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"CorcheteIzquierdo",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"Igual",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"REGISTROS",tmp.linea,tmp.columna)

    def CONTEO(self, nodoInicio, nodoInstruccion):
        tmp = self.tokens.pop()
        if tmp.tipo == "conteo":
            n0 = self.crearNodo('CONTEO')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "ParentesisDerecho":
                    n4 = self.crearNodo('ParentesisDerecho')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "PuntoComa":
                        filas = len(self.lista)
                        columnas = len(self.lista[0])
                        conteo = int(filas)*int(columnas)
                        # print(">>>"+str(conteo))
                        self.stream += "\n>>>" + str(conteo)
                        
                        n7 = self.crearNodo('PuntoComa')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7, n8)
                            
                        n9 = self.crearNodo('INSTRUCCION_CONTEO')
                        self.agregarHijo(n9, n0)
                        self.agregarHijo(n9, n2)
                        self.agregarHijo(n9, n4)
                        self.agregarHijo(n9, n7)
                            
                        self.agregarHijo(self.inicio, nodoInstruccion)
                        self.agregarHijo(nodoInstruccion, n9)
                        self.inicio = nodoInstruccion

                    else:
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"conteo",tmp.linea,tmp.columna)

    def DATOS(self, nodoInicio, nodoInstruccion):
        tmp = self.tokens.pop()
        if tmp.tipo == "datos":
            n0 = self.crearNodo('DATOS')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()

            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()

                if tmp.tipo == "ParentesisDerecho":
                    n4 = self.crearNodo('ParentesisIzquierdo')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()

                    if tmp.tipo == "PuntoComa":
                        self.impTabla()
                        n6 = self.crearNodo('ParentesisIzquierdo')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        
                        n8 = self.crearNodo('INSTRUCCION_DATOS')
                        self.agregarHijo(n8, n0)
                        self.agregarHijo(n8, n2)
                        self.agregarHijo(n8, n4)
                        self.agregarHijo(n8, n6)
                            
                        self.agregarHijo(self.inicio, nodoInstruccion)
                        self.agregarHijo(nodoInstruccion, n8)
                        self.inicio = nodoInstruccion
                        pass
                    else:
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"DATOS",tmp.linea,tmp.columna)

    def PROMEDIO(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "promedio":
            n0 = self.crearNodo('PROMEDIO')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n6 = self.crearNodo('ParentesisDerecho')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.promedio(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>" + resultado
                                n8 = self.crearNodo('PuntoComa')
                                n9 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n8, n9)
                                
                                n10 = self.crearNodo('INSTRUCCION_PROMEDIO')
                                self.agregarHijo(n10, n0)
                                self.agregarHijo(n10, n2)
                                self.agregarHijo(n10, n4)
                                self.agregarHijo(n10, n6)
                                self.agregarHijo(n10, n8)
                                    
                                self.agregarHijo(self.inicio, nodoInstruccion)
                                self.agregarHijo(nodoInstruccion, n10)
                                self.inicio = nodoInstruccion
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"PROMEDIO",tmp.linea,tmp.columna)

    def SUMAR(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "sumar":
            n0 = self.crearNodo('SUMAR')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n6 = self.crearNodo('ParentesisDerecho')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.sumar(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+resultado
                                n8 = self.crearNodo('PuntoComa')
                                n9 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n8, n9)
                                
                                n10 = self.crearNodo('INSTRUCCION_SUMAR')
                                self.agregarHijo(n10, n0)
                                self.agregarHijo(n10, n2)
                                self.agregarHijo(n10, n4)
                                self.agregarHijo(n10, n6)
                                self.agregarHijo(n10, n8)
                                    
                                self.agregarHijo(self.inicio, nodoInstruccion)
                                self.agregarHijo(nodoInstruccion, n10)
                                self.inicio = nodoInstruccion
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"SUMAR",tmp.linea,tmp.columna)

    def CONTARSI(self, nodoInicio, nodoInstruccion):
        campo = None
        valor = None
        tmp = self.tokens.pop()
        if tmp.tipo == "contarsi":
            n0 = self.crearNodo('CONTARSI')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    campo = tmp.lexema
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "Coma":
                        n6 = self.crearNodo('Coma')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "Cadena" or tmp.tipo == "Decimal" or tmp.tipo == "Entero":
                            valor = tmp.lexema
                            n8 = self.crearNodo('Cadena')
                            n9 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n8, n9)
                            tmp = self.tokens.pop()
                            
                            if tmp.tipo == "ParentesisDerecho":
                                n10 = self.crearNodo('ParentesisDerecho')
                                n11 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n10, n11)
                                tmp = self.tokens.pop()
                                
                                if tmp.tipo == "PuntoComa":
                                    resultado = self.funcion.contarSi(self.lista, self.claves, campo, valor)
                                    if resultado is None:
                                        print("No se ha encontrado el campo")
                                    else:
                                        # print(">>>",resultado)
                                        self.stream += "\n>>>"+resultado
                                        
                                        n12 = self.crearNodo('PuntoComa')
                                        n13 = self.crearNodo(tmp.lexema)
                                        self.agregarHijo(n12, n13)
                                        
                                        n14 = self.crearNodo('INSTRUCCION_CONTARSI')
                                        self.agregarHijo(n14, n0)
                                        self.agregarHijo(n14, n2)
                                        self.agregarHijo(n14, n4)
                                        self.agregarHijo(n14, n6)
                                        self.agregarHijo(n14, n8)
                                        self.agregarHijo(n14, n10)
                                        self.agregarHijo(n14, n12)
                                            
                                        self.agregarHijo(self.inicio, nodoInstruccion)
                                        self.agregarHijo(nodoInstruccion, n14)
                                        self.inicio = nodoInstruccion
                                        
                                else:
                                    self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                            else:
                                self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                        else:
                            self.agregarError(tmp.tipo,"Cadena o Decimal o Entero",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"Coma",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"CONTARSI",tmp.linea,tmp.columna)

    def MAX(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "max":
            n0 = self.crearNodo('MAX')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n6 = self.crearNodo('ParentesisDerecho')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.max(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+resultado
                                
                                n8 = self.crearNodo('PuntoComa')
                                n9 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n8, n9)
                                        
                                n10 = self.crearNodo('INSTRUCCION_MAX')
                                self.agregarHijo(n10, n0)
                                self.agregarHijo(n10, n2)
                                self.agregarHijo(n10, n4)
                                self.agregarHijo(n10, n6)
                                self.agregarHijo(n10, n8)
                                            
                                self.agregarHijo(self.inicio, nodoInstruccion)
                                self.agregarHijo(nodoInstruccion, n10)
                                self.inicio = nodoInstruccion
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"MAX",tmp.linea,tmp.columna)

    def MIN(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "min":
            n0 = self.crearNodo('MIN')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n6 = self.crearNodo('ParentesisDerecho')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.min(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+ resultado
                                
                                n8 = self.crearNodo('PuntoComa')
                                n9 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n8, n9)
                                        
                                n10 = self.crearNodo('INSTRUCCION_MIN')
                                self.agregarHijo(n10, n0)
                                self.agregarHijo(n10, n2)
                                self.agregarHijo(n10, n4)
                                self.agregarHijo(n10, n6)
                                self.agregarHijo(n10, n8)
                                            
                                self.agregarHijo(self.inicio, nodoInstruccion)
                                self.agregarHijo(nodoInstruccion, n10)
                                self.inicio = nodoInstruccion
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"MIN",tmp.linea,tmp.columna)

    def REPORTE(self, nodoInicio, nodoInstruccion):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "exportarReporte":
            n0 = self.crearNodo('REPORTE')
            n1 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n0, n1)
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                n2 = self.crearNodo('ParentesisIzquierdo')
                n3 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n2, n3)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    n4 = self.crearNodo('Cadena')
                    n5 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n4, n5)
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        n6 = self.crearNodo('ParentesisDerecho')
                        n7 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n6, n7)
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            reporte = self.reporte.reporteHtml(cadena, self.claves, self.lista)
                            self.stream += reporte
                            
                            n8 = self.crearNodo('PuntoComa')
                            n9 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n8, n9)
                                        
                            n10 = self.crearNodo('INSTRUCCION_REPORTE')
                            self.agregarHijo(n10, n0)
                            self.agregarHijo(n10, n2)
                            self.agregarHijo(n10, n4)
                            self.agregarHijo(n10, n6)
                            self.agregarHijo(n10, n8)
                                            
                            self.agregarHijo(self.inicio, nodoInstruccion)
                            self.agregarHijo(nodoInstruccion, n10)
                            self.inicio = nodoInstruccion
                            
                        else:
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"MIN",tmp.linea,tmp.columna)

    def crearNodo(self,etiqueta : str) -> str:
        id = str(uuid.uuid1())
        self.g.node(id,etiqueta)
        return id

    def agregarHijo(self,id_padre,id_hijo : str):
        self.g.edge(id_padre,id_hijo)

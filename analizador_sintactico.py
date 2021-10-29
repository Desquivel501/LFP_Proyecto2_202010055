from prettytable import PrettyTable
from functions import Functions
from reportes import Reportes

from graphviz import Digraph
import uuid
import copy

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
        tmp = self.tokens[-1]
        while tmp.tipo.upper() not in self.reservadas :
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
        self.INSTRUCCIONES()
        
    def INSTRUCCIONES(self):
        instrucciones = self.crearNodo('INSTRUCCIONES')
        self.agregarHijo(self.inicio, instrucciones)
        self.inicio = instrucciones
        
        self.INSTRUCCION()
        self.INSTRUCCIONES2()

    def INSTRUCCIONES2(self):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo.upper() in self.reservadas:
                self.INSTRUCCION()
                self.INSTRUCCIONES2()
            else:
                self.agregarError(tmp.tipo,"Instruccion",tmp.linea,tmp.columna)
                self.INSTRUCCION()
                self.INSTRUCCIONES2()
        except IndexError:
            pass
        except Exception as e:
            print("Here")
            print(e)
            pass

    def INSTRUCCION(self):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo == 'imprimir':
                self.IMPRIMIR()
            elif tmp.tipo == 'imprimirln':
                self.IMPRIMIRLN()
            elif tmp.tipo == 'Claves':
                self.CLAVES()
            elif tmp.tipo == 'Registros':
                # instruccion = self.crearNodo('INSTRUCCION')
                self.REGISTROS()
            elif tmp.tipo == 'conteo':
                self.CONTEO()
            elif tmp.tipo == 'promedio':
                self.PROMEDIO()
            elif tmp.tipo == 'contarsi':
                self.CONTARSI()
            elif tmp.tipo == 'datos':
                self.DATOS()
            elif tmp.tipo == 'sumar':
                self.SUMAR()
            elif tmp.tipo == 'max':
                self.MAX()
            elif tmp.tipo == 'min':
                self.MIN()
            elif tmp.tipo == 'exportarReporte':
                self.REPORTE()
            else:
                pass
        except IndexError:
            pass
        except Exception as e:
            print("here2")
            print(e)
            pass

    def IMPRIMIR(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimir":
            imprimir = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = copy.deepcopy(tmp.lexema)
                    cadena = cadena.replace('"', '')
                    self.stream += cadena
                    cadena_lxm = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema  
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            nodoInstruccion = self.crearNodo('INSTRUCCION')
                            
                            n0 = self.crearNodo('IMPRIMIR')
                            n10 = self.crearNodo(imprimir)
                            self.agregarHijo(n0, n10)
                            
                            n1 = self.crearNodo('ParentesisIzquierdo')
                            n2 = self.crearNodo(parentesis_i)
                            self.agregarHijo(n1, n2)
                            
                            n3 = self.crearNodo('Cadena')
                            n4 = self.crearNodo(cadena_lxm)
                            self.agregarHijo(n3, n4)
                            
                            n5 = self.crearNodo('ParentesisDerecho')
                            n6 = self.crearNodo(parentesis_d)
                            self.agregarHijo(n5, n6)
                    
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"IMPRIMIR",tmp.linea,tmp.columna)

    def IMPRIMIRLN(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimirln":
            imprimir = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena_lxm = copy.deepcopy(tmp.lexema)
                    cadena = tmp.lexema
                    cadena = cadena.replace('"', '')
                    self.stream += "\n" + cadena
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            nodoInstruccion = self.crearNodo('INSTRUCCION')
                            
                            n0 = self.crearNodo('IMPRIMIRLN')
                            n2 = self.crearNodo(imprimir)
                            self.agregarHijo(n0, n2)
                            
                            n3 = self.crearNodo('ParentesisIzquierdo')
                            n4 = self.crearNodo(parentesis_i)
                            self.agregarHijo(n3, n4)
                            
                            n5 = self.crearNodo('Cadena')
                            n6 = self.crearNodo(cadena_lxm)
                            self.agregarHijo(n5, n6)
                            
                            n7 = self.crearNodo('ParentesisDerecho')
                            n8 = self.crearNodo(parentesis_d)
                            self.agregarHijo(n7, n8)
                            
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"IMPRIMIRLN",tmp.linea,tmp.columna)

    def CLAVES(self):
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
                                self.tokens.append(tmp)
                                self.agregarError(tmp.tipo,"PuntoComa o CorcheteDerecho",tmp.linea,tmp.columna)
                        else:
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
                            break
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"CorcheteIzquierdo",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"Igual",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"CLAVES",tmp.linea,tmp.columna)

        self.claves = temp_row

    def REGISTROS(self):

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
                                        self.tokens.append(tmp)
                                        self.agregarError(tmp.tipo,"Coma o LlaveDerecha",tmp.linea,tmp.columna)
                                        break
                                else:
                                    self.tokens.append(tmp)
                                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
                                    break
                            self.lista.append(temp_row)

                        elif tmp.tipo == "CorcheteDerecho":
                            break
                        else:
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"LlaveIzquierda o CorcheteDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"CorcheteIzquierdo",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"Igual",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"REGISTROS",tmp.linea,tmp.columna)

    def CONTEO(self):
        tmp = self.tokens.pop()
        if tmp.tipo == "conteo":
            conteo = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()
                
                if tmp.tipo == "ParentesisDerecho":
                    parentesis_d = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "PuntoComa":
                        filas = len(self.lista)
                        columnas = len(self.lista[0])
                        conteo = int(filas)*int(columnas)
                        # print(">>>"+str(conteo))
                        self.stream += "\n>>>" + str(conteo)
                        
                        nodoInstruccion = self.crearNodo('INSTRUCCION')
                        
                        n0 = self.crearNodo('CONTEO')
                        n1 = self.crearNodo(conteo)
                        self.agregarHijo(n0, n1)
                        
                        n2 = self.crearNodo('ParentesisIzquierdo')
                        n3 = self.crearNodo(parentesis_i)
                        self.agregarHijo(n2, n3)
                        
                        n4 = self.crearNodo('ParentesisDerecho')
                        n5 = self.crearNodo(parentesis_d)
                        self.agregarHijo(n4, n5)
                        
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
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"conteo",tmp.linea,tmp.columna)

    def DATOS(self):
        tmp = self.tokens.pop()
        if tmp.tipo == "datos":
            datos = tmp.lexema
            tmp = self.tokens.pop()

            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()

                if tmp.tipo == "ParentesisDerecho":
                    parentesis_d = tmp.lexema
                    tmp = self.tokens.pop()

                    if tmp.tipo == "PuntoComa":
                        self.impTabla()
                        
                        nodoInstruccion = self.crearNodo('INSTRUCCION')
                        
                        n0 = self.crearNodo('DATOS')
                        n1 = self.crearNodo(datos)
                        self.agregarHijo(n0, n1)
                        
                        n2 = self.crearNodo('ParentesisIzquierdo')
                        n3 = self.crearNodo(parentesis_i)
                        self.agregarHijo(n2, n3)
                        
                        n4 = self.crearNodo('ParentesisDerecho')
                        n5 = self.crearNodo(parentesis_d)
                        self.agregarHijo(n4, n5)
                        
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
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"DATOS",tmp.linea,tmp.columna)

    def PROMEDIO(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "promedio":
            promedio = tmp.lexema
            
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena_lxm = tmp.lexema
                    cadena = tmp.lexema
                    
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.promedio(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>" + resultado
                                
                                nodoInstruccion = self.crearNodo('INSTRUCCION')
                                
                                n0 = self.crearNodo('PROMEDIO')
                                n1 = self.crearNodo(promedio)
                                self.agregarHijo(n0, n1)
                                
                                n2 = self.crearNodo('ParentesisIzquierdo')
                                n3 = self.crearNodo(parentesis_i)
                                self.agregarHijo(n2, n3)
                                
                                n4 = self.crearNodo('Cadena')
                                n5 = self.crearNodo(cadena_lxm)
                                self.agregarHijo(n4, n5)
                                
                                n6 = self.crearNodo('ParentesisDerecho')
                                n7 = self.crearNodo(parentesis_d)
                                self.agregarHijo(n6, n7)
                                
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"PROMEDIO",tmp.linea,tmp.columna)

    def SUMAR(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "sumar":
            sumar = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena_lxm = tmp.lexema
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.sumar(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+resultado
                                nodoInstruccion = self.crearNodo('INSTRUCCION')
                                
                                n0 = self.crearNodo('SUMAR')
                                n1 = self.crearNodo(sumar)
                                self.agregarHijo(n0, n1)
                                
                                n2 = self.crearNodo('ParentesisIzquierdo')
                                n3 = self.crearNodo(parentesis_i)
                                self.agregarHijo(n2, n3)
                                
                                n4 = self.crearNodo('Cadena')
                                n5 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n4, n5)
                                
                                n6 = self.crearNodo('ParentesisDerecho')
                                n7 = self.crearNodo(parentesis_d)
                                self.agregarHijo(n6, n7)
                                
                                n8 = self.crearNodo('PuntoComa')
                                n9 = self.crearNodo(cadena_lxm)
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"SUMAR",tmp.linea,tmp.columna)

    def CONTARSI(self):
        campo = None
        valor = None
        tmp = self.tokens.pop()
        if tmp.tipo == "contarsi":
            contarsi = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena1 = tmp.lexema
                    campo = tmp.lexema   
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "Coma":
                        coma = tmp.lexema  
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "Cadena" or tmp.tipo == "Decimal" or tmp.tipo == "Entero":
                            valor = tmp.lexema
                            cadena2 = tmp.lexema
                            tmp = self.tokens.pop()
                            
                            if tmp.tipo == "ParentesisDerecho":
                                parentesis_d = tmp.lexema
                                tmp = self.tokens.pop()
                                
                                if tmp.tipo == "PuntoComa":
                                    resultado = self.funcion.contarSi(self.lista, self.claves, campo, valor)
                                    if resultado is None:
                                        print("No se ha encontrado el campo")
                                    else:
                                        # print(">>>",resultado)
                                        self.stream += "\n>>>"+resultado
                                        
                                        nodoInstruccion = self.crearNodo('INSTRUCCION')
                                        
                                        n0 = self.crearNodo('CONTARSI')
                                        n1 = self.crearNodo(contarsi)
                                        self.agregarHijo(n0, n1)
                                        
                                        n2 = self.crearNodo('ParentesisIzquierdo')
                                        n3 = self.crearNodo(parentesis_i)
                                        self.agregarHijo(n2, n3)
                                        
                                        n4 = self.crearNodo('Cadena')
                                        n5 = self.crearNodo(cadena1)
                                        self.agregarHijo(n4, n5)
                                        
                                        n6 = self.crearNodo('Coma')
                                        n7 = self.crearNodo(coma)
                                        self.agregarHijo(n6, n7)
                                        
                                        n8 = self.crearNodo('Cadena')
                                        n9 = self.crearNodo(cadena2)
                                        self.agregarHijo(n8, n9)
                                        
                                        n10 = self.crearNodo('ParentesisDerecho')
                                        n11 = self.crearNodo(parentesis_d)
                                        self.agregarHijo(n10, n11)
                                        
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
                                    self.tokens.append(tmp)
                                    self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                            else:
                                self.tokens.append(tmp)
                                self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                        else:
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"Cadena o Decimal o Entero",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"Coma",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"CONTARSI",tmp.linea,tmp.columna)

    def MAX(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "max":
            max = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema  
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena_lxm = tmp.lexema
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.max(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+resultado
                                
                                nodoInstruccion = self.crearNodo('INSTRUCCION')
                                
                                n0 = self.crearNodo('MAX')
                                n1 = self.crearNodo(max)
                                self.agregarHijo(n0, n1)
                                
                                n2 = self.crearNodo('ParentesisIzquierdo')
                                n3 = self.crearNodo(parentesis_i)
                                self.agregarHijo(n2, n3)
                                
                                n4 = self.crearNodo('Cadena')
                                n5 = self.crearNodo(cadena_lxm)
                                self.agregarHijo(n4, n5)
                                
                                n6 = self.crearNodo('ParentesisDerecho')
                                n7 = self.crearNodo(parentesis_d)
                                self.agregarHijo(n6, n7)
                                
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"MAX",tmp.linea,tmp.columna)

    def MIN(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "min":
            min = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema 
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena_lxm = tmp.lexema
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.min(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                # print(">>>",resultado)
                                self.stream += "\n>>>"+ resultado
                                
                                nodoInstruccion = self.crearNodo('INSTRUCCION')
                                
                                n0 = self.crearNodo('MAX')
                                n1 = self.crearNodo(min)
                                self.agregarHijo(n0, n1)
                                
                                n2 = self.crearNodo('ParentesisIzquierdo')
                                n3 = self.crearNodo(parentesis_i)
                                self.agregarHijo(n2, n3)
                                
                                n4 = self.crearNodo('Cadena')
                                n5 = self.crearNodo(cadena_lxm)
                                self.agregarHijo(n4, n5)
                                
                                n6 = self.crearNodo('ParentesisDerecho')
                                n7 = self.crearNodo(parentesis_d)
                                self.agregarHijo(n6, n7)
                                
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"MIN",tmp.linea,tmp.columna)

    def REPORTE(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "exportarReporte":
            reporte = tmp.lexema
            tmp = self.tokens.pop()
            
            if tmp.tipo == "ParentesisIzquierdo":
                parentesis_i = tmp.lexema 
                tmp = self.tokens.pop()
                
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    cadena_lxm = tmp.lexema
                    tmp = self.tokens.pop()
                    
                    if tmp.tipo == "ParentesisDerecho":
                        parentesis_d = tmp.lexema
                        tmp = self.tokens.pop()
                        
                        if tmp.tipo == "PuntoComa":
                            reporte = self.reporte.reporteHtml(cadena, self.claves, self.lista)
                            self.stream += reporte
                            
                            nodoInstruccion = self.crearNodo('INSTRUCCION')
                                
                            n0 = self.crearNodo('MAX')
                            n1 = self.crearNodo(reporte)
                            self.agregarHijo(n0, n1)
                                
                            n2 = self.crearNodo('ParentesisIzquierdo')
                            n3 = self.crearNodo(parentesis_i)
                            self.agregarHijo(n2, n3)
                                
                            n4 = self.crearNodo('Cadena')
                            n5 = self.crearNodo(cadena_lxm)
                            self.agregarHijo(n4, n5)
                                
                            n6 = self.crearNodo('ParentesisDerecho')
                            n7 = self.crearNodo(parentesis_d)
                            self.agregarHijo(n6, n7)
                                
                            
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
                            self.tokens.append(tmp)
                            self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                    else:
                        self.tokens.append(tmp)
                        self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
                else:
                    self.tokens.append(tmp)
                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
            else:
                self.tokens.append(tmp)
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.tokens.append(tmp)
            self.agregarError(tmp.tipo,"MIN",tmp.linea,tmp.columna)

    def crearNodo(self,etiqueta : str) -> str:
        id = str(uuid.uuid1())
        self.g.node(id,etiqueta)
        return id

    def agregarHijo(self,id_padre,id_hijo : str):
        self.g.edge(id_padre,id_hijo)

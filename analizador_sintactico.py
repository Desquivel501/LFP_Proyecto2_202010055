from prettytable import PrettyTable
from functions import Functions

class AnalizadorSintactico:
    
    def __init__(self,tokens = []):
        self.errores = []
        self.tokens = tokens
        self.tokens.reverse()
        self.reservadas = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR", "PUNTOCOMA"]
        self.lista = []
        self.claves = []
        self.funcion = Functions()
        
    def agregarError(self,obtenido,esperado,fila,columna):
        self.errores.append(
            "<ERROR SINTÁCTICO> Se obtuvo {}, se esperaba {}. Fila: {}, Columna: {}".format(
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
            print(x)   

    def impTabla(self):
        x = PrettyTable()
        x.field_names = self.claves
        if len(self.lista)==0:
            print('No hay Valores')
        else:
            for i in self.lista:
                x.add_row(i)
            print(x)     
            
    def analizar(self):
        self.INICIO()
        self.impErrores()
        
        
    def INICIO(self):
        self.INSTRUCCIONES()
        
    def INSTRUCCIONES(self):
        self.INSTRUCCION()
        self.INSTRUCCIONES2()
        
    def INSTRUCCIONES2(self):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo.upper() in self.reservadas:
                self.INSTRUCCION()
                self.INSTRUCCIONES2()
            else:
                pass
        except IndexError:
            pass
        except Exception as e: 
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
            else:
                pass
        except IndexError:
            pass
        except Exception as e: 
            print(e)
            pass
    
    def IMPRIMIR(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimir":
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    cadena = cadena.replace('"', '')
                    print(cadena , end =" ")
                    tmp = self.tokens.pop()
                    if tmp.tipo == "ParentesisDerecho":
                        tmp = self.tokens.pop()
                        if tmp.tipo == "PuntoComa":
                            pass
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
            
    def IMPRIMIRLN(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimirln":
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    cadena = cadena.replace('"', '')
                    print()
                    print(cadena)
                    tmp = self.tokens.pop()
                    if tmp.tipo == "ParentesisDerecho":
                        tmp = self.tokens.pop()
                        if tmp.tipo == "PuntoComa":
                            pass
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
        print(self.claves)
        
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
            self.agregarError(tmp.tipo,"REGITROS",tmp.linea,tmp.columna)
            
    def CONTEO(self):
        tmp = self.tokens.pop()
        if tmp.tipo == "conteo":
            
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                
                tmp = self.tokens.pop()
                if tmp.tipo == "ParentesisDerecho":
                    
                    tmp = self.tokens.pop()
                    if tmp.tipo == "PuntoComa":
                        filas = len(self.lista)
                        columnas = len(self.lista[0])
                        conteo = int(filas)*int(columnas)
                        print(conteo)
                        
                    else:
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"conteo",tmp.linea,tmp.columna)

    def DATOS(self):
        tmp = self.tokens.pop()
        if tmp.tipo == "datos":
            tmp = self.tokens.pop()

            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()

                if tmp.tipo == "ParentesisDerecho":
                    tmp = self.tokens.pop()

                    if tmp.tipo == "PuntoComa":
                        self.impTabla()
                    else:
                        self.agregarError(tmp.tipo,"PuntoComa",tmp.linea,tmp.columna)
                else:
                    self.agregarError(tmp.tipo,"ParentesisDerecho",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"ParentesisIzquierdo",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"conteo",tmp.linea,tmp.columna)

    def PROMEDIO(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "promedio":
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "ParentesisDerecho":
                        tmp = self.tokens.pop()
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.promedio(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                print(resultado)
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
        
    def SUMAR(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "sumar":
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()
                if tmp.tipo == "Cadena":
                    cadena = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "ParentesisDerecho":
                        tmp = self.tokens.pop()
                        if tmp.tipo == "PuntoComa":
                            resultado = self.funcion.sumar(self.lista, self.claves, cadena)
                            if resultado is None:
                                print("No se ha encontrado el campo")
                            else:
                                print(resultado)
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
    
    def CONTARSI(self):
        campo = None
        valor = None
        tmp = self.tokens.pop()
        if tmp.tipo == "contarsi":
            tmp = self.tokens.pop()
            if tmp.tipo == "ParentesisIzquierdo":
                tmp = self.tokens.pop()
                if tmp.tipo == "Cadena":
                    campo = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "Coma":
                        tmp = self.tokens.pop()
                        if tmp.tipo == "Cadena" or tmp.tipo == "Decimal" or tmp.tipo == "Entero":
                            valor = tmp.lexema
                            tmp = self.tokens.pop()
                            if tmp.tipo == "ParentesisDerecho":
                                tmp = self.tokens.pop()
                                if tmp.tipo == "PuntoComa":
                                    resultado = self.funcion.contarSi(self.lista, self.claves, campo, valor)
                                    if resultado is None:
                                        print("No se ha encontrado el campo")
                                    else:
                                        print(resultado)
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
            self.agregarError(tmp.tipo,"IMPRIMIR",tmp.linea,tmp.columna)


                    

                    
                            
                            
                    
                
from prettytable import PrettyTable

class AnalizadorSintactico:
    
    def __init__(self,tokens = []):
        self.errores = []
        self.tokens = tokens
        self.tokens.reverse()
        self.reservadas = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR", "PUNTOCOMA"]
        self.lista = []
        
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
        except:
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
            else:
                pass
        except:
            pass
    
    def IMPRIMIR(self):
        cadena = None
        tmp = self.tokens.pop()
        if tmp.tipo == "IMPRIMIR":
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
        if tmp.tipo == "IMPRIMIRLN":
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
            self.agregarError(tmp.tipo,"IMPRIMIR",tmp.linea,tmp.columna)
           
                
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
            
        self.lista.append(temp_row)
        print(temp_row)
        
        
        
    def REGISTROS(self):
        
    #añadir corchete derecho
        tmp = self.tokens.pop()
        if tmp.tipo == "Claves":
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
                                else:
                                    self.agregarError(tmp.tipo,"Cadena",tmp.linea,tmp.columna)
                                    break
                            self.lista.append(temp_row)
                            
                        else:
                            self.agregarError(tmp.tipo,"LlaveIzquierda",tmp.linea,tmp.columna)
             
                else:
                    self.agregarError(tmp.tipo,"CorcheteIzquierdo",tmp.linea,tmp.columna)
            else:
                self.agregarError(tmp.tipo,"Igual",tmp.linea,tmp.columna)
        else:
            self.agregarError(tmp.tipo,"CLAVES",tmp.linea,tmp.columna)
            
        self.lista.append(temp_row)
        print(temp_row)
                    
                            
                            
                    
                
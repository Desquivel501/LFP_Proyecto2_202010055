from Token import Token
from Error import Error
from prettytable import PrettyTable

class AnalizadorLexico:

    def __init__(self):
        self.reservadas = ["CLAVES", "REGISTROS", "IMPRIMIR", "IMPRIMIRLN", "CONTEO", "PROMEDIO", "CONTARSI", "DATOS", "MAX", "MIN", "EXPORTARREPORTE", "SUMAR"]
        self.simbolos = [";", ",", "=", "{", "}", "[", "]", "(", ")"]
        self.listaTokens = [] 
        self.listaErrores = []
        self.linea = 1
        self.columna = 1
        self.buffer = ''
        self.bufferError= ""
        self.estado = 0
        self.i = 0
        self.errores = []
        
    def agregarToken(self, caracter, token, linea, columna):
        self.listaTokens.append(Token(caracter,token,linea,columna))
        self.buffer = ''
    
    def agregar_error(self,caracter,linea,columna):
        self.listaErrores.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', linea, columna))
        self.buffer = ''
        
        self.errores.append(
            "<ERROR LEXICO> Caracter {} no reconocido en el lenguaje. Fila: {}, Columna: {}".format(
                caracter,
                linea,
                columna
            )
        )
        
    def estado0(self, caracter):
        if caracter.isalpha():
            self.buffer += caracter 
            self.columna += 1
            self.estado = 1
            
        elif caracter.isdigit():
            self.buffer += caracter 
            self.columna += 1
            self.estado = 2
            
        elif caracter in self.simbolos:
            self.detectarSimbolo(caracter)
            
        elif caracter == '"':
            self.buffer += caracter
            self.columna += 1
            self.estado = 5
        
        elif caracter == "#":
            self.columna += 1
            self.estado = 7
        
        elif caracter == "'":
            self.buffer += caracter
            self.columna += 1
            self.estado = 9
            
        elif caracter == '\n':
            self.linea += 1
            self.columna = 1
            
        elif caracter in ['\t',' ']:
            self.columna += 1      
            
        elif caracter == '\r':
            pass
        
        else:
            self.buffer += caracter
            self.agregar_error(self.buffer,self.linea,self.columna)
            self.columna += 1 
        
      
    def estado1(self,caracter):
        if caracter.isalpha():
            self.buffer +=caracter
            self.columna += 1  
        
        else:
            if self.palabraReservada():
                self.agregarToken(self.buffer.strip(), self.buffer.strip(), self.linea, self.columna)
                self.estado = 0
                self.columna+=1
                self.i -= 1
            
            else:
                # self.agregar_error(self.buffer, self.linea, self.columna)
                # self.estado = 0
                # self.columna+=1
                # self.i -= 1 
                
                self.agregarToken(self.buffer.strip(), "Texto" , self.linea, self.columna)
                self.estado = 0
                self.columna+=1
                self.i -= 1
                
    def estado2(self,caracter):
        if caracter.isdigit():
            self.buffer+=caracter
            self.columna+=1
            
        elif caracter == ".":
            self.buffer+=caracter
            self.columna+=1
            self.estado = 3
            
        else:
            self.agregarToken(self.buffer,'Entero',self.linea,self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1
            
    def estado3(self,caracter):
        if caracter.isdigit():
            self.buffer+=caracter
            self.columna+=1
        else:
            self.agregarToken(self.buffer,'Decimal',self.linea,self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1
            
    def estado5(self,caracter):
        if caracter != "\"":           
            self.buffer +=caracter
            self.columna += 1 
        else:
            self.buffer +=caracter
            self.agregarToken(self.buffer, "Cadena", self.linea, self.columna)
            self.estado = 0
            self.columna+=1    
    
    def estado7(self,caracter):
        if caracter == '\n':
            self.estado = 0
            self.linea+=1
            self.columna = 1
        else:
            self.columna+=1
            
    def estado9(self,caracter):
        if caracter == "'":
            self.buffer += caracter
            self.estado = 10
            self.columna+=1
        else: 
            self.agregar_error(self.buffer, self.linea, self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1 
    
    def estado10(self,caracter):
        if caracter == "'":
            self.buffer += caracter
            self.estado = 11
            self.columna+=1
        else: 
            self.agregar_error(self.buffer, self.linea, self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1 
    
    def estado11(self,caracter):
        if caracter == "'":
            self.buffer += caracter
            self.estado = 12
            self.columna+=1
        elif caracter == '\n':
            self.buffer += caracter
            self.linea+=1
            self.columna = 1
        else:
            self.buffer += caracter
            self.columna+=1
    
    def estado12(self,caracter):
        if caracter == "'":
            self.buffer += caracter
            self.estado = 13
            self.columna+=1
        else: 
            self.agregar_error(self.buffer, self.linea, self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1 
            
    def estado13(self,caracter):
        if caracter == "'":
            self.buffer = ""
            self.estado = 0
            self.columna+=1
        else: 
            self.agregar_error(self.buffer, self.linea, self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1 

    def detectarSimbolo(self,caracter):
        if caracter == ";":
            self.agregarToken(str(caracter), "PuntoComa", self.linea, self.columna)
        elif caracter == ",":
            self.agregarToken(str(caracter), "Coma", self.linea, self.columna)
        elif caracter == "=":
            self.agregarToken(str(caracter), "Igual", self.linea, self.columna)
        elif caracter == "{":
            self.agregarToken(str(caracter), "LlaveIzquierda", self.linea, self.columna)
        elif caracter == "}":
            self.agregarToken(str(caracter), "LlaveDerecha", self.linea, self.columna)
        elif caracter == "[":
            self.agregarToken(str(caracter), "CorcheteIzquierdo", self.linea, self.columna)
        elif caracter == "]":
            self.agregarToken(str(caracter), "CorcheteDerecho", self.linea, self.columna)
        elif caracter == "(":
            self.agregarToken(str(caracter), "ParentesisIzquierdo", self.linea, self.columna)
        elif caracter == ")":
            self.agregarToken(str(caracter), "ParentesisDerecho", self.linea, self.columna)
                
        self.buffer = ''
        self.columna+=1
        
    def palabraReservada(self):
        if self.buffer.upper() in self.reservadas:
            return True
        else:
            return False  
            
          
    def analizar(self,cadena):
        self.listaTokens = [] 
        self.listaErrores = []
        self.i = 0
        
        while self.i < len(cadena):
            if self.estado == 0:
                self.estado0(cadena[self.i])
            elif self.estado == 1:
                self.estado1(cadena[self.i])
            elif self.estado == 2:
                self.estado2(cadena[self.i])
            elif self.estado == 3:
                self.estado3(cadena[self.i])
            elif self.estado == 5:
                self.estado5(cadena[self.i])
            elif self.estado == 7:
                self.estado7(cadena[self.i])
            elif self.estado == 9:
                self.estado9(cadena[self.i])
            elif self.estado == 10:
                self.estado10(cadena[self.i])
            elif self.estado == 11:
                self.estado11(cadena[self.i])
            elif self.estado == 12:
                self.estado12(cadena[self.i])
            elif self.estado == 13:
                self.estado13(cadena[self.i])
            self.i += 1
        
        return (self.listaTokens,self.listaErrores, self.errores)
    
        
    def impTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema", "Token", "Fila", "Columna"]
        for i in self.listaTokens:
            x.add_row(i.enviar())
        print(x)

    def impErrores(self):
        x = PrettyTable()
        x.field_names = ["Descripcion", "Fila", "Columna"]
        if len(self.listaErrores)==0:
            print('No hay errores')
        else:
            for i in self.listaErrores:
                x.add_row(i.enviar())
            print(x)
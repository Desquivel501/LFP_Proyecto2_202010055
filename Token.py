class Token:
    
    def __init__(self, lexema, tipo, linea, columna):
        self.lexema = lexema
        self.tipo = tipo
        self.columna = columna
        self.linea = linea
    
    def imprimir(self):
        print(self.lexema, self.tipo, self.linea, self.columna)
    
    def enviar(self):
        return [self.lexema, self.tipo, self.linea, self.columna]

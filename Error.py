class Error:
    
    def __init__(self, descripcion, linea, columna):
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
    
    def imprimir(self):
        print(self.descripcion, self.columna, self.linea)
    
    def enviar(self):
        return [self.descripcion, self.columna, self.linea]
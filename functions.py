class Functions:
    
    def __init__(self):
        pass

    def promedio(self, registros, claves, campo):
        cadena = campo.replace('"', '')
        cont=0
        found=False
        largo = len(registros)

        for val in claves:
            
            if val == cadena:

                found = True
                break
            cont+=1
        if found:
            suma = 0
            i = 0
            while largo>i:
                suma += float(registros[i][cont])
                i += 1
            total = float(suma)/float(i)
            return str(total)
        else:
            return None
        
    def sumar(self, registros, claves, campo):
        cadena = campo.replace('"', '')
        cont=0
        largo = len(registros)

        for val in claves:
            if val == cadena:
                suma = 0
                i = 0
                while largo>i:
                    suma += float(registros[i][cont])
                    i += 1
                return str(suma)
            cont+=1
        return None    
    
    def contarSi(self, registros, claves, campo, valor):
        cadena = campo.replace('"', '')
        cont=0
        found=False
        largo = len(registros)
        for val in claves:
            if val == cadena:
                found = True
                break
            cont+=1
        if found:
            suma = 0
            i = 0
            while largo>i:
                if registros[i][cont] == valor:
                    suma += 1
                i += 1
            return str(suma)
        else:
            return None

    def max(self, registros, claves, campo):
        cadena = campo.replace('"', '')
        max = 0
        cont=0
        largo = len(registros)
        
        for val in claves:
            if val == cadena:
                i = 0
                while largo>i:
                    if float(registros[i][cont]) > max:
                        max = float(registros[i][cont])
                    i += 1
                return str(max)
            cont+=1
        return None
      
    def min(self, registros, claves, campo):
        cadena = campo.replace('"', '')
        min = float('inf')
        cont=0
        largo = len(registros)
        
        for val in claves:
            if val == cadena:
                i = 0
                while largo>i:
                    if float(registros[i][cont]) < min:
                        min = float(registros[i][cont])
                    i += 1
                return str(min)
            cont+=1
        return None

        



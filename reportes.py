import os

class Reportes:
    
    def __init__(self):
        pass

    def reporteHtml(self, titulo, registros, claves):
        
        html =  """<!doctype html>
                    <html lang="en">
                    <head>
                    <!-- Required meta tags -->
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                    <!-- Bootstrap CSS -->
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

                    <title>Reportes</title>
                    </head>
                    <body>
                
                    &nbsp;
                    <h1 style="text-align: center;"> """+ str(titulo) + """</h1>
                    <&nbsp;<                     

                    <table style="height: 108px; width: 60%; border-collapse: collapse; margin-left: auto; margin-right: auto;" class="table table-striped">
                    <thead class="table-dark">
                    <tr style="height: 18px;">"""
        
        for reg in registros:
            html +='<th><strong>'+ str(reg) +'</strong></th>'
  
        html+= """  </tr>
                    </thead>
                    <tbody>
                    """
                    
        for fila in claves:
            html += """<tr style="height: 18px;">"""
            for columna in fila:
                html += """<td>""" + str(columna) +"""</span></td>"""                
                    
            html +="""</tr>"""
                    
         
        html += """ </tbody>
                    </table>"""
        
        cwd = os.getcwd()
        archivo = open("Reporte.html","w+")
        archivo.write(html)
        # print(">>>Se ha generado el reporte en: " + cwd + "\Reporte.html")
        return "\n>>>Se ha generado el reporte en: " + cwd + "\Reporte.html"
        archivo.close()
        # os.startfile("Reporte.html")
        

                        
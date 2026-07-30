# etapa_5

en_prueba = False

if en_prueba:
    codigo_a_procesar = []

def indentacion(codigo):

    nuevo_codigo = []
    esp = 1
    tab = 4

    for lineas in codigo:
        tokens, NDL = lineas

        nueva_linea = []
        historial = []
        indent = True
        nivel = 0
        total_esp = 0
        total_tab = 0
        total = 0
        totaltotal = 0

        for token in tokens:
            t = token["t"]
            
            if indent:
                
                if t in (" ", "\t"):
                    if t == " ":
                        total_esp += esp
                        totaltotal+= esp
                        if total_esp == 4:
                            nivel += 1
                            total_esp = 0
                    else:
                        total_tab += tab
                        totaltotal+= tab
                        nivel += 1
                    historial.append(t)
                    continue
                else:
                    total+=total_esp
                    total+=total_tab
                    if (total % 4) == 0:
                        indent = False
                    else:
                        return ["ERR", {"SUB": "ET5", "ERROR": {"tipo": "IndentacionInvalida", "total_tabesp": totaltotal, "historial": historial, "linea": NDL}}]
            nueva_linea.append(token)

        if nueva_linea:
            nuevo_codigo.append([nivel, nueva_linea, NDL])
        continue

    return ["OK", nuevo_codigo]

if en_prueba:
    print(indentacion(codigo_a_procesar))

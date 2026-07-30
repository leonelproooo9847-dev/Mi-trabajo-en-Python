# etapa_8

en_prueba = False

if en_prueba:
    prueba = []
    # colocar estructura

def secuencia_de_tokens(codigo):
    
    sec_tokens = []

    tips_anid = (
        "APAR",
        "CPAR",
        "ALLV",
        "CLLV",
        "ABLQ",
        "CBLQ"
    )

    profundidad = 0

    pila_anid   = []
    pila_indent = [0]

    for lineas in codigo:

        INDENT, TOKENS, NDL = lineas

        sec_tokens.append(["NVL", NDL])

        if profundidad == 0:
            nivel = pila_indent[-1]
            
            if INDENT > nivel:
                pila_indent.append(INDENT)
                sec_tokens.append(["INDENT"])
            
            if INDENT < nivel:
                encontrado = False
                i_ = len(pila_indent)-1
                while i_ >= 0:
                    NDI_ = pila_indent[i_]
                    if NDI_ == INDENT:
                        encontrado = True
                        break
                    else:
                        pila_indent.pop()
                        sec_tokens.append(["DESINDENT"])
                    i_-=1

                if not encontrado:
                    return ["ERR", "INFO_0"] # indentación mal formada

        for token in TOKENS:
            # la variable "t" no se utiliza
            tipo =  token["tipo"]
            colum = token["columna"]

            if tipo in tips_anid:
                if tipo in ("APAR", "ALLV", "ABLQ"):
                    profundidad += 1
                    pila_anid.append([tipo, colum, NDL])
                else:
                    if pila_anid:
                        arpertura = pila_anid.pop()
                        tipo_a, ub_c, ub_l = arpertura

                        if tipo_a == "APAR" and tipo != "CPAR":
                            return ["ERR", {"SUB": "ET8", "ERROR": {"tipo": "MalaEstructuraDeParentesis", "columna": [ub_c, colum], "linea": [ub_l, NDL]}}]
                        elif tipo_a == "ALLV" and tipo != "CLLV":
                            return ["ERR", {"SUB": "ET8", "ERROR": {"tipo": "MalaEstructuraDeLlaves", "columna": [ub_c, colum], "linea": [ub_l, NDL]}}]
                        elif tipo_a == "ABLQ" and tipo != "CBLQ":
                            return ["ERR", {"SUB": "ET8", "ERROR": {"tipo": "MalaEstructuraDeCorchetes", "columna": [ub_c, colum], "linea": [ub_l, NDL]}}]
                        else:
                            profundidad-=1
                            if profundidad < 0:
                                profundidad = 0
                    else:
                        return ["ERR", {"SUB": "ET8", "ERROR": {"tipo": "CierreSinApertura", "columna": colum, "linea": NDL}}] # error por cierre sin apertura.
            
            sec_tokens.append(["TOKEN", token])
    if pila_anid:
        arpertura = pila_anid.pop()
        tipo_a, ub_c, ub_l = arpertura
        return ["ERR", {"SUB": "ET8", "ERROR": {"tipo": "AperturaSinCierre", "columna": ub_c,"linea": ub_l}}] # error por apertura sin cierre
    else:
        if pila_indent:
            nivel = pila_indent[-1]
            if 0 < nivel:
                i_ = len(pila_indent)-1
                while i_ >= 0:
                    NDI_ = pila_indent[i_]
                    if NDI_ == 0:
                        break
                    else:
                        pila_indent.pop()
                        sec_tokens.append(["DESINDENT"])
                    i_-=1

        sec_tokens.append(["FIN"])
    

    return ["OK", sec_tokens]

if en_prueba:
    resultado = secuencia_de_tokens(prueba)
    print(resultado)

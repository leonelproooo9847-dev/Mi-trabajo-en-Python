# etapa_2

en_prueba = False

if en_prueba:
    codigo_a_procesar = []

def agrupador(codigo):

    SIMB = (
        # comunes:
        ".", ",", "*", "/",
        "+", "-", "¿", "?",
        ":", ";", "¡", "!",
        "'", '"', "^", "=",
        "<", ">",
        
        # estructuras de anidamientos:
        "(", ")", "[", "]",
        "{", "}",
        
        # simbolos exóticos:
        "#", "%", "@", "`",
    )

    secuencias_esc = {
        "n": ["\\n", "US_NVL"],
        "t": ["\\t", "US_TAB"],
        "r": ["\\r", "US_RET"],
        '"': ['\\"', "US_DCM"],
        "\\": ["\\\\", "US_BAR"]
    }


    nuevo_codigo = []

    for lineas in codigo:

        tokens, NDL = lineas

        if tokens == "NULO":
            continue
        
        columna = 0
        pos_anterior = None
        nueva_linea = []
        temporal = []

        es_escape = False

        for token in tokens:
            columna+=1
            if es_escape:
                if token in secuencias_esc:
                    if temporal:
                        pal = "".join(temporal)
                        temporal = []
                        nueva_linea.append({"t": pal, "tipo": None, "columna": pos_anterior})
                        pos_anterior = None
                    token_esc = secuencias_esc[token][0]
                    tipo_esc = secuencias_esc[token][1]
                    nueva_linea.append({"t": token_esc, "tipo": tipo_esc, "columna": columna-1})
                else:
                    if token in (" ", "\t"):
                        return ["ERR", {"SUB": "ET2", "ERROR": {"tipo": "SecuenciaEscCortada", "columna": columna, "linea": NDL}}]
                    return ["ERR", {"SUB": "ET2", "ERROR": {"tipo": "SecuenciaEscInvalida", "columna": columna, "linea": NDL}}]
                es_escape = False
                continue

            if token == "\\":
                es_escape = True
                continue

            if token in SIMB or token in (" ", "\t"):
                if temporal:
                    pal = "".join(temporal)

                    if pal == "_": # excepciones:
                        nueva_linea.append({"t": pal, "tipo": "SIMB", "columna": pos_anterior})
                    else:
                        nueva_linea.append({"t": pal, "tipo": None, "columna": pos_anterior})

                    pos_anterior = None
                    temporal = []
                if token in SIMB:
                    nueva_linea.append({"t": token, "tipo": "SIMB", "columna": columna})
                else:
                    if token == " ":
                        nueva_linea.append({"t": token, "tipo": "ESP", "columna": columna})
                    else:
                        nueva_linea.append({"t": token, "tipo": "TAB", "columna": columna})
                continue
            else:
                temporal.append(token)
                if pos_anterior is None:
                    pos_anterior = columna
            
        if es_escape:
            return ["ERR", {"SUB": "ET2", "ERROR": {"tipo": "SecuenciaEscCortada", "columna": columna, "linea": NDL}}]
        if temporal:
            pal = "".join(temporal)

            if pal == "_": # excepciones:
                nueva_linea.append({"t": pal, "tipo": "SIMB", "columna": pos_anterior})
            else:
                nueva_linea.append({"t": pal, "tipo": None, "columna": pos_anterior})

            temporal = []

        nuevo_codigo.append([nueva_linea, NDL])

    return ["OK", nuevo_codigo]

if en_prueba:
    print(agrupador(codigo_a_procesar))

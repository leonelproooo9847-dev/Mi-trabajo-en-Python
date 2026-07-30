# etapa_3

en_prueba = False

if en_prueba:
    codigo_a_procesar = [
        "ingresar producto del procesado 'etapa_2' aquí"
    ]

def cadenas_txt(codigo):
    
    esc = {
        "US_NVL": "\n",
        "US_TAB": "\t",
        "US_RET": "\r",
        "US_DCM": "\"",
        "US_BAR": "\\"
    }

    nuevo_codigo = []

    for lineas in codigo:
        tokens, NDL = lineas

        nueva_linea = []
        cadena = []
        es_cadena = False
        pos = 0

        for token in tokens:
            t = token["t"]
            tipo = token["tipo"]
            columna = token["columna"]
            if es_cadena:
                if t == '"':
                    txt = "".join(cadena)
                    nueva_linea.append({"t": txt, "tipo": "CADENA", "columna": pos})
                    cadena = []
                    es_cadena = False
                    pos = 0
                else:
                    if tipo in esc:
                        cadena.append(esc[tipo])
                    else:
                        cadena.append(t)
                continue
            if t == '"':
                es_cadena = True
                pos = columna
                continue
            else:
                nueva_linea.append(token)
        
        if es_cadena:
            return ["ERR", {"SUB": "ET3", "ERROR": {"tipo": "CadenaNoCerrada", "columna": pos, "linea": NDL}}]
        else:
            nuevo_codigo.append([nueva_linea, NDL])

    return ["OK", nuevo_codigo]

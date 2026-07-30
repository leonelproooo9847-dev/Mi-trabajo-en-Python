# etapa_6

en_prueba = False

if en_prueba:
    codigo_a_procesar = []
    # colocar estructura

def simb_compuestos(codigo):

    nuevo_codigo = []

    for lineas in codigo:
        indent, tokens, NDL = lineas

        nueva_linea = []
        es_cmp = False
        compuesto = []
        pos = 0

        for token in tokens:
            t = token["t"]
            tipo = token["tipo"]
            columna = token["columna"]

            if es_cmp:
                if tipo == "SIMB":
                    compuesto.append(t)
                    continue
                else:
                    nuevo_simb = "".join(compuesto)
                    compuesto = []
                    if len(nuevo_simb) == 1:
                        # caso 1
                        nueva_linea.append({"t": nuevo_simb, "tipo": "SIMB", "columna": pos})
                    elif len(nuevo_simb) == 2:
                        # caso 2 
                        if nuevo_simb in ("==", "<=", ">=", "<<", ">>", "!=", "!!", "??", "::"):
                            nueva_linea.append({"t": nuevo_simb, "tipo": "COMP", "columna": pos})
                        else:
                            # excepción
                            return ["ERR", {"SUB": "ET6", "ERROR": {"tipo": "CompuestoInvalido", "fallo": nuevo_simb, "columna": pos, "linea": NDL}}]
                    else:
                        # excepción
                        return ["ERR", {"SUB": "ET6", "ERROR": {"tipo": "CompuestoDesconocido", "fallo": nuevo_simb, "columna": pos, "linea": NDL}}]
                    pos = 0
                    es_cmp = False
                    nuevo_simb = None
                    nueva_linea.append(token)
                    continue

            if tipo == "SIMB":
                if t in ("=", "<", ">", "!", "?", ":"):
                    compuesto.append(t)
                    pos = columna
                    es_cmp = True
                    continue
                
            nueva_linea.append(token)
        
        if es_cmp:
            nuevo_simb = "".join(compuesto)
            compuesto = []
            if len(nuevo_simb) == 1:
                nueva_linea.append({"t": nuevo_simb, "tipo": "SIMB", "columna": pos})
            elif len(nuevo_simb) == 2:
                if nuevo_simb in ("==", "<=", ">=", "<<", ">>", "!=", "!!", "??", "::"):
                    nueva_linea.append({"t": nuevo_simb, "tipo": "COMP", "columna": pos})
                else:
                    return ["ERR", {"SUB": "ET6", "ERROR": {"tipo": "CompuestoInvalido", "fallo": nuevo_simb, "columna": pos, "linea": NDL}}]
            else:
                return ["ERR", {"SUB": "ET6", "ERROR": {"tipo": "CompuestoDesconocido", "fallo": nuevo_simb, "columna": pos, "linea": NDL}}]
            pos = 0
            es_cmp = False
            nuevo_simb = None

        nuevo_codigo.append([indent, nueva_linea, NDL])

    return ["OK", nuevo_codigo]

if en_prueba:
    print(simb_compuestos(codigo_a_procesar))

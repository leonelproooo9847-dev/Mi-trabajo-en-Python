# etapa_7

en_prueba = False

if en_prueba:
    codigo_a_procesar = None
    # colocar estructura

def tipos(codigo):

    nuevo_codigo = []


    # especiales del lenguaje:
    #############################################################
    palabras_clv = (        # etiquetado como 'PCLV'
        # variables:
        "CREAR", "BORRAR",
        
        # palabras condicionales:
        "SI", "SINO", "SINO_SI", 

        # entrada y salida:
        "LEER", "MOSTRAR", "IMPRIMIR",

        # bucles:
        "MIENTRAS", "POR",

        # depuradores:
        "MEMORIA", "VER"
    )

    ObjetosProto = (        # etiquetado como 'OBJET'
        "ENT",
        "FLOT",
        "BOOL",
        "CADENA",
        "INDEF"
    )

    OperadoresLogicos = (   # etiquetado como 'OP_LOG'
        "_O_",
        "_Y_",
        "_NO_"
    )

    palabras_booleanas = (  # etiquetado como 'BOOL'
        "VERDAD",      "FALSO"
    #   Verdadero      Falso
    )
    #############################################################

    # simbolos en general
    #############################################################
    SIMB_GNRAL = {
        # simbolos:
        ".": "PUNT",    # punto
        ",": "COMA",    # coma
        "¿": "AINT",    # apertura  interrogación
        "?": "CINT",    # cierre    interrogación
        ":": "DPUN",    # doble punto
        ";": "PCOM",    # punto y coma
        "¡": "AEXC",    # apertura  exclamación
        "!": "CEXC",    # cierre    exclamación
        "'": "UCOM",    # una       comilla
        '"': "DCOM",    # doble     comilla
        "=": "IGUA",    # igual
        "@": "ARRO",    # arroba
        "`": "COMI",    # coma invertida
        "<": "MENA",    # menor a
        ">": "MAYA",    # mayor a

        # operadores:
        "+": "SUMA",    # sumador
        "-": "GUIO",    # guion
        "*": "ASTE",    # asterisco
        "/": "BARR",    # barra
        "%": "MODU",    # modulo
        "^": "CIRC",    # circunflejo

        # exclusivos:
        "_": "BBAJ"     # barra baja
    }

    anidamientos = {
        "(": "APAR",    # apertura  parentesis
        ")": "CPAR",    # cierre    parentesis
        "{": "ALLV",    # apertura  llaves
        "}": "CLLV",    # cierre    llaves
        "[": "ABLQ",    # apertura  bloque
        "]": "CBLQ"     # cierre    bloque
    }

    compuestos = {
        "==": "IGIG",   # igual igual   a
        "<=": "MEIG",   # menor o igual a
        ">=": "MAIG",   # mayor o igual a
        "!=": "DSTN",   # distindo de
        "!!": "DISV",   # distinto valor
        "??": "DIST",   # distinto tipo
        "::": "DDPU",   # doble doble punto
        "<<": "DESI",   # desplazamiento a izquierda
        ">>": "DESD"    # desplazamiento a derecha
    }
    #############################################################

    for lineas in codigo:
        indent, tokens, NDL = lineas

        nueva_linea = []

        for token in tokens:
            t = token["t"]
            tipo = token["tipo"]
            columna = token["columna"]

            if tipo == "ESP" or tipo == "TAB":
                continue

            if tipo == "SIMB":
                if t in anidamientos:
                    nueva_linea.append({"t": t, "tipo": anidamientos[t], "columna": columna})
                elif t in SIMB_GNRAL:
                    nueva_linea.append({"t": t, "tipo": SIMB_GNRAL[t], "columna": columna})
                continue
            if tipo == "COMP":
                if t in compuestos:
                    nueva_linea.append({"t": t, "tipo": compuestos[t], "columna": columna})
                continue

            if tipo is None:
                if t in palabras_clv:
                    nueva_linea.append({"t": t, "tipo": "PCLV", "columna": columna})
                elif t in palabras_booleanas:
                    nueva_linea.append({"t": t, "tipo": "BOOL", "columna": columna})
                elif t in ObjetosProto:
                    nueva_linea.append({"t": t, "tipo": "OBJET", "columna": columna})
                elif t in OperadoresLogicos:
                    nueva_linea.append({"t": t, "tipo": "OP_LOG", "columna": columna})
                else:
                    es_letra = False
                    primero = 0
                    for c in t:
                        if c in "1234567890":
                            if primero == 0:
                                primero = 1
                        else:
                            es_letra = True
                            if primero == 0:
                                primero = 2
                    if primero == 1:
                        if es_letra:
                            return ["ERR", {"SUB": "ET7", "ERROR": {"tipo": "LetrasEnUnDecimal", "fallo": t, "columna": columna, "linea": NDL}}]
                        nueva_linea.append({"t": t, "tipo": "ENT", "columna": columna})
                    elif primero == 2:
                        if es_letra:
                            nueva_linea.append({"t": t, "tipo": "IDENT", "columna": columna})
                        else:
                            return ["ERR", {"SUB": "ET7", "ERROR": {"tipo": "Extraño", "fallo": t, "columna": columna, "linea": NDL}}]
            else:
                nueva_linea.append(token)
            continue
        
        nuevo_codigo.append([indent, nueva_linea, NDL])
    
    return ["OK", nuevo_codigo]

if en_prueba:
    print(tipos(codigo_a_procesar))

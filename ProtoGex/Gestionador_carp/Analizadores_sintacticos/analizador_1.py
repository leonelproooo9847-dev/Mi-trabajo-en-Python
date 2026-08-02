# analizador_1.py

en_prueba = True

if en_prueba:
    prueba = [
        ['NVL', 1], 
        ['TOKEN', {'t': 'X', 'tipo': 'IDENT', 'columna': 1}], 
        ['TOKEN', {'t': '=', 'tipo': 'IGUA', 'columna': 3}], 
        ['TOKEN', {'t': '3', 'tipo': 'ENT', 'columna': 5}], 
        ['TOKEN', {'t': '+', 'tipo': 'SUMA', 'columna': 7}], 
        ['TOKEN', {'t': '4', 'tipo': 'ENT', 'columna': 9}], 
        ['TOKEN', {'t': '*', 'tipo': 'ASTE', 'columna': 11}], 
        ['TOKEN', {'t': '_NO_', 'tipo': 'OP_LOG', 'columna': 13}], 
        ['TOKEN', {'t': '2', 'tipo': 'ENT', 'columna': 18}], 
        ['FIN']
    ]

if False: # solo comentarios multilineas.

    # """': solo para comentarios.
    # '''": para representar estructuras.
    """'
        Esta analización del parser no intenta ver el contexto o de toda la
        expresión, verificar si un operador puede operar con un INDEF u otras cosas,
        su trabajo es simple. Verificar si la secuencia entra en las secuencias
        gramáticas formales ya descritas en EXP. No intenta ver el contexo, solo
        verificar, por esta razón este proceso no modificaría la estructura, solo
        la observa.
    '"""

    """'
        Dado a esto, debo aclarar 2 cosas fundamentales de mi lexer:

        El lexer ya resuelve lo que es los anidamientos, es decir, ya da aviso
        de errores como: "[...}", "...]", "[ ... (...]", etc. por lo tanto,
        el parser no debe preocuparse por la estructura anidadas porque eso ya
        viene garantizado por el lexer.

        Además secuencias unarias como "-3" y "+4" o "+3.1416" y "-23.65" también
        vienen garantizado por el lexer, y lo engloba todo en un único tipo común:
        el ENT y el FLOT. (bueno... debería. Porque en realidad no está implementado,
        pero imaginemos que tenemos la realidad distorsionada y que sí lo hace).
    '"""

    '''"
        EXP = {
            "C1": (_VALOR_, _OP_),
            "C2": (_OP_NO_),
            "C3": (_ANID_, "EXP", _ANID_)
        }
    "'''

    '''"programa a prueba:
    SI  (
        (2 = 3)
        _O_
        (
            VERDAD 
            _Y_
            _NO_ 
        )
    )
    "'''

def validador(
    secuencia: list,
):
    if not isinstance(secuencia, list):
        raise TypeError(f"'secuencia' debe ser list, pero es {type(secuencia)}")

    _OP_NO_ = (
        "OP_LOG",   # este es el tipo.
        "_NO_"      # este no es el tipo, es el texto (o "valor")
    )

    _VALOR_ = (
        # literales
        "PCLV",     "BOOL",     "ENT", 
        "FLOT",     "CADENA",   "INDEF",
        "IDENT",    "OBJET"
    )

    _OP_ = (
        "PUNT",     # punto                      .
        "COMA",     # coma                       ,
        "AINT",     # apertura  interrogación    ¿
        "CINT",     # cierre    interrogación    ?
        "DPUN",     # doble punto                :
        "PCOM",     # punto y coma               ;
        "AEXC",     # apertura  exclamación      ¡
        "CEXC",     # cierre    exclamación      !
        "UCOM",     # una       comilla          '
        "DCOM",     # doble     comilla          "
        "IGUA",     # igual                      =
        "ARRO",     # arroba                     @
        "COMI",     # coma invertida             `
        "MENA",     # menor a                    <
        "MAYA",     # mayor a                    >

        # operadores:
        "SUMA",     # sumador                    +
        "GUIO",     # guion                      -
        "ASTE",     # asterisco                  *
        "BARR",     # barra                      /
        "MODU",     # modulo                     %
        "CIRC",     # circunflejo                ^

        # exclusivos:
        "BBAJ",     # barra baja                 _

        "IGIG",   # 'igual igual   a'            ==
        "MEIG",   # 'menor o igual a'            <=
        "MAIG",   # 'mayor o igual a'            >=
        "DSTN",   # 'distindo de'                !=
        "DISV",   # 'distinto valor'             !!
        "DIST",   # 'distinto tipo'              ??
        "DDPU",   # 'doble doble punto'          ::
        "DESI",   # 'desplazamiento a izquierda' <<
        "DESD",   # 'desplazamiento a derecha'   >>

        # operador lógico
        "OP_LOG"  # _O_, _Y_, _NO_
    )

    _ANID_ = (
        "APAR",     # apertura  parentesis
        "CPAR",     # cierre    parentesis
        "ALLV",     # apertura  llaves
        "CLLV",     # cierre    llaves
        "ABLQ",     # apertura  bloque
        "CBLQ"      # cierre    bloque
    )

    def acceder(
        token_: dict
    ):
        if not isinstance(token_, dict):
            raise TypeError(f"'token_' debe ser dict, pero es {type(token_)}")
        return token_["t"], token_["tipo"], token_["columna"]

    # elementos:
    FIN         = "FIN"
    NVL         = "NVL"
    TOKEN       = "TOKEN"
    INDENT      = "INDENT"
    DESINDENT   = "DESINDENT"

    EXPRESION_BINARIA   = 1 # expresiones binarias: 2 + 3
    EXPRESION_LOG_NO    = 2 # expresiones del NO lógico (not): _NO_ (...)
    EXPRESION_ANIDADA   = 3 # expresiones de anidamientos: ( ... ), [ ... ], { ... }

    CASO_ACTUAL = EXPRESION_BINARIA

    # caso 1 (EXPRESION_BINARIA)
    ES_VALOR = True

    termino = True

    i = 0
    longitud = len(secuencia)

    linea_actual = 0
    columna_actual = 0

    while i < longitud:
        elemento = secuencia[i]

        tipo_de_elemento = elemento[0]

        if tipo_de_elemento == NVL:
            valor = elemento[1]
            linea_actual = valor
            if termino:
                termino = False
                i += 1 # avanzo al siguiente
                continue
            else:
                return ["ERR", {"ERR_1"}]

        elif tipo_de_elemento == TOKEN:
            valor = elemento[1]

            t, tipo, columna_actual = acceder(valor)

            if CASO_ACTUAL == EXPRESION_BINARIA:
                if tipo in _VALOR_ and ES_VALOR:
                    termino = True
                    ES_VALOR = False
                    i += 1 # avanzo al siguiente
                elif tipo in _OP_ and not ES_VALOR:
                    termino = False
                    ES_VALOR = True
                    i += 1 # avanzo al siguiente
                else:
                    # si el fallo ocurrió cuando esperaba un operando:
                    if ES_VALOR:
                        # verifico si:
                        #     es una expresion de aninamiento
                        #     o una expresion de NO lógico (not)
                        termino = False

                        if tipo in _ANID_:
                            CASO_ACTUAL = EXPRESION_ANIDADA
                        elif tipo in _OP_NO_:
                            CASO_ACTUAL = EXPRESION_LOG_NO
                        else:
                            return ["CTO", {"EXTRAÑO_1"}]
                        continue

                    # si, en cambio, ocurrió cuando esperaba un operador:
                    elif not ES_VALOR:
                        # entonces espero una expresion de anidamiento
                        termino = False
                        CASO_ACTUAL = EXPRESION_ANIDADA
                        continue

            elif CASO_ACTUAL == EXPRESION_LOG_NO:
                if tipo in _OP_NO_ and t in _OP_NO_:
                    i += 1 # avanzo al siguiente
                    elemento = secuencia[i]
                    
                    tipo_de_elemento = elemento[0]

                    if tipo_de_elemento != TOKEN:
                        return ["ERR", {"EXPRESION_NO_LOG_INCOMPLETA"}]
                    else:
                        valor = elemento[1]
                        
                        t, tipo, columna_actual = acceder(valor)

                        if tipo in _VALOR_:
                            termino = True
                            ES_VALOR = False
                            CASO_ACTUAL = EXPRESION_BINARIA
                            i += 1 # avanzo al siguiente
                        elif tipo in _ANID_:
                            termino = False
                            CASO_ACTUAL = EXPRESION_ANIDADA        
                            return ["DP", {"desde": "EXPRESION_LOG_NO", "PASAR": CASO_ACTUAL}]
                        
                        continue
                else:
                    return ["CTO", "EXTRAÑO_2"]
                    

        elif tipo_de_elemento == FIN:
            if termino:
                return ["OK", {"EXPRESION_VALIDA"}]
            else:
                return ["ERR", {"EXPRESION_INCOMPLETA"}]
        else:
            return ["ERR", {"TIPO_ELEMENTO_EXTRAÑO"}]


if en_prueba:
    print(validador(prueba))

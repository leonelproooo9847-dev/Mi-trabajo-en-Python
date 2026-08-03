# analizador_1.py

en_prueba = False

if en_prueba:
    prueba = None

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
        Tuve un cambio de perspectiva. En vez de hacer un autómata que solo reconoce
        en qué estado se encuentra, decidí hacer un autómata que decida seguhn el token
        vió anteriormente.

        Si vio VALOR:
            ANID (APER)     :   OK
            ANID (CIER)     :   OK
            OP              :   OK
            NO_LOG          :   NO
            VALOR           :   NO  (puede que lo cambie)

        Si vio OP:
            VALOR           :   OK
            NO_LOG          :   OK
            ANID (APER)     :   OK
            ANID (CIER)     :   NO
            OP              :   NO
        
        Si vio NO_LOG:
            VALOR           :   OK
            ANID (APER)     :   OK
            ANID (CIER)     :   NO
            OP              :   NO
            NO_LOG          :   NO

        Si vio ANID:
            (APER):
                ANID (APER) :   OK
                ANID (CIER) :   OK
                NO_LOG      :   OK
                VALOR       :   OK
                OP          :   NO
            (CIER):
                ANID (APER) :   OK
                ANID (CIER) :   OK
                OP          :   OK
                VALOR       :   NO
                NO_LOG      :   NO
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

    profundidad = 0
    termino = True
    memoria = None

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
            if termino or profundidad != 0:
                if profundidad == 0:
                    memoria = None
                termino = False
                i += 1 # avanzo al siguiente
                continue
            else:
                return ["ERR", "LINEA_INCOMPLETA"]

        elif tipo_de_elemento == TOKEN:
            valor = elemento[1]

            t, tipo, columna_actual = acceder(valor)
            
            
            if memoria is not None:
                t_, tipo_, columna_ = acceder(memoria)
                
                if tipo_ in _VALOR_:
                    if tipo in _OP_:
                        termino = False
                    elif tipo in _ANID_:
                        if tipo in ("APAR", "ALLV", "ABLQ"):
                            termino = False
                            profundidad += 1
                        else:
                            termino = True
                            profundidad -= 1
                    else:
                        return ["ERR", "a1"]
                
                elif tipo_ in _OP_:
                    if tipo in _VALOR_:
                        termino = True
                    elif tipo in _ANID_:
                        if tipo in ("APAR", "ALLV", "ABLQ"):
                            termino = False
                            profundidad += 1
                        else:
                            return ["ERR", "02"]
                    elif tipo in _OP_NO_ and t in _OP_NO_:
                        termino = False
                    else:
                        return ["ERR", "a2"]
                
                elif tipo_ in _OP_NO_ and t_ in _OP_NO_:
                    if tipo in _VALOR_:
                        termino = True
                    elif tipo in _ANID_:
                        if tipo in ("APAR", "ALLV", "ABLQ"):
                            termino = False
                            profundidad += 1
                        else:
                            return ["ERR", "03"]
                    else:
                        return ["ERR", "a3"]
                
                elif tipo_ in _ANID_:
                    if tipo_ in ("APAR", "ALLV", "ABLQ"):
                        if tipo in _ANID_:
                            if tipo in ("APAR", "ALLV", "ABLQ"):
                                termino = False
                                profundidad += 1
                                # aumento profundidad
                            else:
                                termino = False
                                profundidad -= 1
                                # disminuyo profundidad
                        elif tipo in _VALOR_:
                            termino = False
                        elif tipo in _OP_NO_ and t in _OP_NO_:
                            termino = False
                        else:
                            return ["ERR", "a4"]
                    else:
                        if tipo in _ANID_:
                            if tipo in ("APAR", "ALLV", "ABLQ"):
                                termino = False
                                profundidad += 1
                                # aumento profundidad
                            else:
                                termino = True
                                profundidad -= 1
                                # disminuyo profundidad
                        elif tipo in _OP_:
                            termino = False
                        else:
                            return ["ERR", "b4"]
            
            if (tipo in _OP_ and t not in _OP_NO_) and memoria is None:
                return ["ERR", "a5"]
            else:
                memoria = valor
        
        if tipo_de_elemento == FIN:
            if termino:
                return ["OK", "SINTAXIS_VALIDA"]
            else:
                return ["ERR", "EXP_INCOMPLETA"]
        
        i+=1


if en_prueba:
    print(validador(prueba))

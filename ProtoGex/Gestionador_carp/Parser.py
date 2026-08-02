import traceback

en_prueba = True

if en_prueba:
    prueba = None

def parser(
    data: list
):
    if data is not isinstance(data, list):
        raise TypeError(f"PARSER: Objeto invalido, es esperaba una lista y apareció: {type(data)}")
    
    return 0
    
    '''
    EXP:
        CASO_1: VALOR, (OP, VALOR)*
        CASO_2: OP_LOG_NO, EXP
        CASO_3: (ANID, EXP, ANID)*

    todavía sin procesos
    '''

# analizador_2.py

en_prueba = False

if en_prueba:
    prueba = None

def arbol_sintactico(
    secuencia_tokens: list
):
    if not isinstance(secuencia_tokens, list):
        raise TypeError(f"'secuencia_tokens' debe ser list, pero es {type(secuencia_tokens)}")


    for elemento in secuencia_tokens:
        valor = elemento[0]

    return 0

    '''"
        Gramatica:

            CREAR -> :: -> EXP_CREAR

            EXP_CREAR:
                IDENT, (COMA, IDENT)*

            
            SI/SINO_SI/MIENTRAS  -> ( -> EXP -> ) -> BLOQUE_INDENT

            SINO -> BLOQUE_INDENT

            continua...
    "'''

if en_prueba:
    print(arbol_sintactico(prueba))

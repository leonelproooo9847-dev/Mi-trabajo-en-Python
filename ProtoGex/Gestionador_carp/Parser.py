import traceback

en_prueba = False
cambiar_entorno = False


if en_prueba:
    prueba = None

if cambiar_entorno:
    from Analizadores_sintacticos.analizador_1 import validador
else:
    from .Analizadores_sintacticos.analizador_1 import validador

def parser(
    secuencia: list
):
    if not isinstance(secuencia, list):
        raise TypeError(f"PARSER: Objeto invalido, es esperaba una lista y apareció: {type(secuencia)}")
    
    try:
        resultado = validador(secuencia)

        rcode = resultado[0]

        if rcode == "ERR":
            return resultado
        else:
            return resultado
    except Exception:
        traceCTOVL = traceback.format_exc()
        return ["CTO", {"ORIGEN": "Parser", "SUB": "ANLIZ_1"}, traceCTOVL]

if en_prueba:
    print(parser(prueba))

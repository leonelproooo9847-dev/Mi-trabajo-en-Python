# Gestionador.py

import traceback

en_prueba = False
cambiar_entorno = False

# cambiar_entorno = True:
#     se exportan modulos desde el punto de perspectiva de Gestionador.
# cambiar_entorno = False:
#     se exportan modulos desde la perspectiva del Ejecutor.

if cambiar_entorno:
    from Tokenizador import tokenizador
    from Parser import parser
    from ModulErr import Err, mensaje_imprimible
    from ModulCTO import CTO_str
else:
    from .Tokenizador import tokenizador
    from .Parser import parser
    from .ModulErr import Err, mensaje_imprimible
    from .ModulCTO import CTO_str

if en_prueba:
    ruta = "C:\\Users\\Usuario\\Desktop\\ProtoGex\\Entorno ProtoGex.txt"

    with open(ruta, "r", encoding="utf-8") as leer:
        texto_crudo = leer.read()

def ejecutar_ModulErr(
    informacion_ERR: dict,
    estructura:  list
):
    if not isinstance(informacion_ERR, dict):
        raise TypeError(f"'informacion_ERR' debe ser dict, pero es {type(informacion_ERR)}")
    if not isinstance(estructura, list):
        raise TypeError(f"'estructura' debe ser list, pero es: {type(estructura)}")
    
    # lógica:
    try:
        mensaje_ERR = Err(informacion_ERR, estructura)
        mensaje_ERR = mensaje_imprimible(mensaje_ERR)
        return mensaje_ERR, None
    except Exception:
        traceCTOMR = traceback.format_exc()
        return None, ["CTO", {"ORIGEN": "Gestionador", "SUB": "ModulErr"}, traceCTOMR]

def ejecutar_ModulCTO(
    informacion_CTO: list
):
    if not isinstance(informacion_CTO, list):
        raise TypeError(f"'informacion_CTO' debe ser list, pero es {type(informacion_CTO)}")
    
    try:
        mensaje_CTO = CTO_str(informacion_CTO)
        return mensaje_CTO
    except Exception:
        traceCTOMC = traceback.format_exc()
        return f"\x1b[31;1m[CTO2]:\xb1[31m\n\tocurrió un problema en el módulo ModulCTO.py en el Gestionador.py\n\n\tdatos:\n\t\t{traceCTOMC}\x1b[0m"
    

def Gestionar(
    texto_crudo: str
):
    if not isinstance(texto_crudo, str):
        raise TypeError(f"texto_crudo de tipo str, apareció: {type(texto_crudo)}")

    guardado = None

    # tokenizador:
    # ===============================================================
    # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    try:
        resultado_lexer, cto_lexer, _ = tokenizador(texto_crudo)
        # resultado_lexer: [rcode, datos, estructura_extra]
        # cto_lexer:       ["CTO", {...}, traceback]
        # _:               depurador

        if cto_lexer is not None:  # CRITICO!!!
            return ["CTO", ejecutar_ModulCTO(cto_lexer)]
        else:
            rcode, data, guardado = resultado_lexer

            if rcode == "ERR":
                r_mr, cto_mr = ejecutar_ModulErr(data, guardado)
                if cto_mr is not None:
                    return ["CTO", ejecutar_ModulCTO(cto_mr)]
                else:
                    return ["ERR", r_mr]
            if rcode in ("VACIO", "OK"):
                if rcode == "VACIO":
                    return [rcode, data]
                
                

    except Exception:
        traceCTO_TOKENIZADOR = traceback.format_exc()
        return ["CTO", ejecutar_ModulCTO(["CTO", {"ORIGEN": "Gestionador", "SUB": "Tokenizador"}, traceCTO_TOKENIZADOR])]
    # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    # ===============================================================




    # parse:
    # ===============================================================
    # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    try:
        resultado_parser = parser(data)

        rcode = resultado_lexer[0]

        if rcode == "ERR":
            return resultado_parser
        else:
            return resultado_parser
    except Exception:
        traceCTO_PARSER = traceback.format_exc()
        return ["CTO", ejecutar_ModulCTO(["CTO", {"ORIGEN": "Gestionador", "SUB": "Parser"}, traceCTO_PARSER])]

    # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    # ===============================================================



if en_prueba:
    print(Gestionar(texto_crudo))

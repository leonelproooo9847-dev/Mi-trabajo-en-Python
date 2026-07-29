import traceback

en_prueba = False
cambiar_entorno = False      # cambiar_entorno cuando pruebe en el ejecutór

# probar en ejecutor:                           cambiar_entorno = False
# probar en gestionador o tokenizador mismo:    cambiar_entorno = True

if cambiar_entorno:
    from Analizadores_lexicos.etapa_1 import linea
    from Analizadores_lexicos.etapa_2 import agrupador
    from Analizadores_lexicos.etapa_3 import cadenas_txt
    from Analizadores_lexicos.etapa_4 import eliminar_comentario
    from Analizadores_lexicos.etapa_5 import indentacion
    from Analizadores_lexicos.etapa_6 import simb_compuestos
    from Analizadores_lexicos.etapa_7 import tipos
    from Analizadores_lexicos.etapa_8 import secuencia_de_tokens
else:
    from .Analizadores_lexicos.etapa_1 import linea
    from .Analizadores_lexicos.etapa_2 import agrupador
    from .Analizadores_lexicos.etapa_3 import cadenas_txt
    from .Analizadores_lexicos.etapa_4 import eliminar_comentario
    from .Analizadores_lexicos.etapa_5 import indentacion
    from .Analizadores_lexicos.etapa_6 import simb_compuestos
    from .Analizadores_lexicos.etapa_7 import tipos
    from .Analizadores_lexicos.etapa_8 import secuencia_de_tokens

if en_prueba:
    ruta = "C:\\Users\\Usuario\\Desktop\\Proto-Ajust\\ProtoGex Entorno.txt"

    with open(ruta, "r", encoding="utf-8") as leer:

        texto_crudo = leer.read()

def tokenizador(texto: str):
    
    '''
    procesos:
        _ 1 = líneas
        _ 2 = agrupación y secuencias de escape
        _ 3 = cadenas textuales
        _ 4 = eliminar comentarios
        _ 5 = indentación
        _ 6 = identificar simbolos compuestos
        _ 7 = identificar tipos
        _ 8 = convertir estructura a una linea de tokens
        otros procesos de refinado...
    '''

    proceso = 0
    data = texto
    guardado = None

    errno = [
        None,
        "ET2",
        "ET3",
        "ET4",
        "ET5",
        "ET6",
        "ET7",
        "ET8"
    ]

    funcion = [
        # esta etapa_1 nunca devolverá error porque su trabajo es solamente
        # normalizar el texto, separando caracteres y lineas.
        linea,                  # 0 (1)
        agrupador,              # 1 (2)
        cadenas_txt,            # 2 (3)
        eliminar_comentario,    # 3 (4)
        indentacion,            # 4 (5)
        simb_compuestos,        # 5 (6)
        tipos,                  # 6 (7)
        secuencia_de_tokens     # 7 (8)
    ]

    # depurador:
    parar = False
    donde = 1
    
    while proceso <= 7:

        proc = funcion[proceso]

        try:
            output = proc(data)

            rcode, data = output

            if rcode in "ERR":
                data["ORIGEN"] = "Tokenizador"
                return [rcode, data, guardado], None, None
            elif proceso == 0:
                guardado = data
            
            proceso+=1
        except Exception:
            traceCTO_SUBPROCESO = traceback.format_exc()
            return None, ["CTO", {"ORIGEN": "Tokenizador", "SUB": errno[proceso]}, traceCTO_SUBPROCESO], None
        
        if parar:
            if donde == proceso:
                return None, None, ["DP", data]
    
    if len(data) == 1:
        return ["VACIO", None, None], None, None

    return ["OK", data, guardado], None, None

if en_prueba:
    resultado, cto, dp = tokenizador(texto_crudo)
    print(resultado)
    print(cto)
    print(dp)

# ModulCTO.py

en_prueba = False

if en_prueba:
    data = []
    """estructura exigida
    [
        'CTO',
        {
            'ORIGEN': ...,
            'SUB':    ...
        },
        Traceback_de_python
    ]
    """

def CTO_str(
    cto_estructura: list
):
    origen = None
    subproceso = None

    if len(cto_estructura) >= 1:
        elemento_1 = cto_estructura[0] # ==> "CTO"
        mensaje = f"\x1b[31;1m[{elemento_1}]\x1b[0m:\x1b[31m\n\t"
    else:
        mensaje = "\x1b[31;1m[???]\x1b[0m:\x1b[31m\n\t"
    mensaje += "Ocurrió un error en el sistema, este error no está relacionado con su programa.\n\n\t"

    if len(cto_estructura) >= 2:
        elemento_2 = cto_estructura[1] # ==> diccionario (dict)
        if not isinstance(elemento_2, dict):
            raise TypeError(f"'elemento_2' debe ser dict, pero es {type(elemento_2)}")
    else:
        mensaje += "No hay datos de ubicación exacta.\x1b[0m"
        return mensaje
    
    if "ORIGEN" in elemento_2:
        origen = elemento_2["ORIGEN"]
    if "SUB" in elemento_2:
        subproceso = elemento_2["SUB"]

    if origen is not None:
        mensaje += f"Origen: {origen}\n\t"
    if subproceso is not None:
        mensaje += f"Subproceso: {subproceso}\n\n\t"
    else:
        mensaje += "\n\t"
    
    if len(cto_estructura) == 3:
        elemento_3 = cto_estructura[2]
        mensaje += "\x1b[35;1mEl error comunica\x1b[0m:\n\t\t"
        mensaje += elemento_3
    else:
        mensaje += "No hay datos del error especifico en el sistema."
    
    mensaje += "\x1b[0m"

    return mensaje

if en_prueba:
    print(CTO_str(data))

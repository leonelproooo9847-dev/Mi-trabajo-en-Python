# etapa_4

en_prueba = False

if en_prueba:
    codigo_a_procesar = [
        "ingrese estructura para depurar"
    ]

def eliminar_comentario(codigo):

    nuevo_codigo = []
    
    ignorar = False
    tipo = 0
    pos = 0

    for lineas in codigo:
        tokens, NDL = lineas

        nueva_linea = []

        for token in tokens:
            t = token["t"]
            if ignorar:
                if tipo == 1:
                    if t == "#":
                        ignorar = False
                        tipo = 0
                continue

            if t in ("#", ";"):
                if t == "#":
                    ignorar = True
                    tipo = 1
                    pos = NDL
                else:
                    ignorar = True
                    tipo = 2
                    pos = NDL
                continue

            nueva_linea.append(token)

        if tipo == 2:
            ignorar = False
            tipo = 0

        if nueva_linea:
            nuevo_codigo.append([nueva_linea, NDL])
    
    if ignorar:
        return ["ERR", {"SUB": "ET4", "ERROR": {"tipo": "ComentarioAbierto", "linea": pos}}]

    return ["OK", nuevo_codigo]


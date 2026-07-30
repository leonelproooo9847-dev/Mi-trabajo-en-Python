# ModulErr.py

en_prueba = False

if en_prueba:
    fallo_pros = None
    guardado = None

def fragmento(
    guardado: list,
    linea_err: int,
    manera:    int = None
):
    
    linea_cod = ""

    for lineas in guardado:

        tokens, NDL = lineas

        if NDL < linea_err:
            continue
        elif NDL > linea_err:
            break
        
        if manera is None:
            for token in tokens:
                linea_cod+=token
        else:
            for token in tokens:
                if token == "\t":
                    linea_cod+="\\t"
                else:
                    linea_cod+=token

    return linea_cod


def Err(
    fallo:                  dict,
    estructura_guardado:    list
):
    
    PORTIPO = 1
    PORTPFN = 2
    PORESPA = 3
    NINGUNO = None

    origen = fallo["ORIGEN"]
    linea_codigo = None

    diccionario = {
        "Tokenizador": {
            "ET2": {
                "SecuenciaEscCortada": [
                    "La secuencia de escape no ha sido terminada correctamente.",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ],

                "SecuenciaEscInvalida": [
                    "La secuencia de escape es invalida.",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ]
            },
            "ET3": {
                "CadenaNoCerrada": [
                    "La cadena textual no ha sido cerrada correctamente.",       
                    "Revisa en la línea: ", 
                    "Y en la columna: "
                ]
            },
            "ET4": {
                "ComentarioAbierto": [
                    "El comentario de texto no ha sido cerrado correctamente.", 
                    "La última apertura se produjo en la línea: "
                ]
            },
            "ET5": {
                "IndentacionInvalida": [
                    "La indentación es incorrecta.", 
                    "No cumple la regla de multiplos de 4:", 
                    "Un espacio vale 1.", 
                    "Una tabulación vale 4.", 
                    "El historial de indentación muestra: ", 
                    "En este caso, el total vale: ",
                    "Revisa en la línea: "
                ]
            },
            "ET6": {
                "CompuestoInvalido": [
                    "El símbolo compuesto formado es invalido: ",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ],

                "CompuestoDesconocido": [
                    "El símbolo compuesto formado no encaja en la gramatica del lenguaje: ",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ]
            },
            "ET7": {
                "LetrasEnUnDecimal": [
                    "El lenguaje clasificó el elemento como una secuencia de dígitos, pero encontró letras.",
                    "El error es: ",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ],

                "Extraño": [
                    "Una excepción extraña.",
                    "Fallo: "
                    "Línea: ",
                    "Columna: "
                ]
            },
            "ET8": {
                "MalaEstructuraDeParentesis": [
                    "La estructura no cierra con un parentesis.", 
                    "Revisa en las líneas: ", 
                    "Y las columnas: "
                ],

                "MalaEstructuraDeLlaves": [
                    "La estructura no cierra con un llaves.", 
                    "Revisa en las líneas: ", 
                    "Y las columnas: "
                ],

                "MalaEstructuraDeCorchetes": [
                    "La estructura no cierra con un corchetes.", 
                    "Revisa en las líneas: ", 
                    "Y las columnas: "
                ],

                "CierreSinApertura": [
                    "Quedó un cierre de más sin apertura.",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ],

                "AperturaSinCierre": [
                    "Quedó una apertura sin cerrar.",
                    "Revisa en la línea: ",
                    "Y en la columna: "
                ]
            }
        }
    }


    if origen == "Tokenizador":
        paquete_de_etapas = diccionario[origen]

        subproceso = fallo["SUB"]
        tipos_msjs = paquete_de_etapas[subproceso]
        ERROR = fallo["ERROR"]
        tipo = ERROR["tipo"]

        mensaje = tipos_msjs[tipo].copy()

        #==========================================

        if subproceso == "ET2":
            linea = ERROR["linea"]
            columna = ERROR["columna"]

            # completado:
            mensaje[1]+=str(linea)
            mensaje[2]+=str(columna)

            linea_codigo = fragmento(estructura_guardado, linea)
            
        elif subproceso == "ET3":
            linea = ERROR["linea"]
            columna = ERROR["columna"]

            # completado:
            mensaje[1]+=str(linea)
            mensaje[2]+=str(columna)

            linea_codigo = fragmento(estructura_guardado, linea)

        elif subproceso == "ET4":
            linea = ERROR["linea"]

            # completado:
            mensaje[1]+=str(linea)

            linea_codigo = fragmento(estructura_guardado, linea)
            
        elif subproceso == "ET5":
            linea = ERROR["linea"]
            historial = ERROR["historial"]
            total = ERROR["total_tabesp"]

            # completado:
            ac = 0
            for carac in historial:
                if ac != 0:
                    mensaje[4]+=", "
                if carac == "\t":
                    mensaje[4]+="\\t"
                else:
                    mensaje[4]+=f"'{carac}'"
                ac+=1
            mensaje[5]+=str(total)
            mensaje[6]+=str(linea)

            linea_codigo = fragmento(estructura_guardado, linea, 1)
            
        elif subproceso == "ET6":
            linea = ERROR["linea"]
            columna = ERROR["columna"]
            el_error = ERROR["fallo"]

            # completado:
            mensaje[0]+=f"'{el_error}'"
            mensaje[1]+=str(linea)
            mensaje[2]+=str(columna)
                
            linea_codigo = fragmento(estructura_guardado, linea)

        elif subproceso == "ET7":
            linea = ERROR["linea"]
            columna = ERROR["columna"]
            el_error = ERROR["fallo"]

            # completado:
            mensaje[1]+=el_error
            mensaje[2]+=str(linea)
            mensaje[3]+=str(columna)

            linea_codigo = fragmento(estructura_guardado, linea)

        elif subproceso == "ET8":
            linea = ERROR["linea"]
            columna = ERROR["columna"]

            if tipo.startswith("MalaEstructuraDe"):
                mensaje[1]+=f"{linea[0]} y {linea[1]}."
                mensaje[2]+=f"{columna[0]} y {columna[1]}"
            else:
                mensaje[1]+=str(linea)
                mensaje[2]+=str(columna)

            linea_codigo = "<SinFormatoParaMostrar>"

        return {
                # primero origen:
                "sub":      subproceso,
                "origen":   origen,
                "tipo":     tipo,

                # segundo mostrado:
                "codigo":   linea_codigo,

                # tercero didactico:
                "mensaje":  mensaje
            }


def mensaje_imprimible(
    conjunto_datos: dict
):
    if not isinstance(conjunto_datos, dict):
        raise TypeError(f"'conjunto_datos' debe ser dict, pero es {type(conjunto_datos)}")
    
    mensaje_str = "\x1b[31;1m[ERR]\x1b[0m:\x1b[31m\n\t"
    
    origen = conjunto_datos["origen"]

    if origen == "Tokenizador":
        mensaje_str+=f"Origen: {origen}\n\t"

        subproceso = conjunto_datos["sub"]
        mensaje_str+=f"Subproceso: {subproceso}\n\n\t"

        tipo = conjunto_datos["tipo"]
        mensaje_str+=f"\x1b[35;1m{tipo}\x1b[0m:\x1b[31m\n\t\t"

        codigo = conjunto_datos["codigo"]
        mensaje_str+=f"|{codigo}\n\n\t"

        data_msj = conjunto_datos["mensaje"]
        ac = 0
        for partes in data_msj:
            if ac != 0:
                mensaje_str+="\n\t"
            mensaje_str+=partes
            ac+=1
        mensaje_str+="\x1b[0m"
    
    return mensaje_str
    
if en_prueba:
    print(mensaje_imprimible(Err(fallo_pros, guardado)))

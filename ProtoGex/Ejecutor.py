# Ejecutor.py

import traceback
import sys
from pathlib import Path

from Gestionador_carp.Gestionador import Gestionar, ejecutar_ModulCTO

def imprimir_ERR(err: str):
    print(err)
def imprimir_CTO(CTO: str):
    print(CTO)

carpeta = Path(__file__).parent

archivo_txt = carpeta / "Entorno ProtoGex.txt"
ruta = str(archivo_txt)

with open(ruta, "r", encoding="utf-8") as archivo:
    ProtoGex = archivo.read()

# EL EJECUTOR EMPIEZA AQUÍ.
# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
def ejecutar(entorno):

    try: # probamos
        Resultado = Gestionar(entorno)
        # estructura [CODIGO_DE_RETORNO, DATOS]

        rcode = Resultado[0]

        # Los datos devueltos con el tipo de retorno:
        #     ERR y CTO
        # son str.

        # Los datos devueltos con OK es la estructura
        # y secuencias de tokens producidos por el lexer.

        if rcode == "ERR":
            imprimir_ERR(Resultado[1])
        elif rcode == "CTO":
            imprimir_CTO(Resultado[1])
        elif rcode == "OK":
            print(Resultado[1])
        else:
            sys.exit()
    except Exception:
        traceCTOGS = traceback.format_exc()
        imprimir_CTO(ejecutar_ModulCTO(["CTO", {"ORIGEN": "EjecP", "SUB": "Gestionador"}, traceCTOGS]))

ejecutar(ProtoGex)
# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

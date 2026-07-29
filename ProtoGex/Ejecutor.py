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

archivo_txt = carpeta / "ProtoGex Entorno.txt"
ruta = str(archivo_txt)

archivo_gestor = carpeta / "Gestionador" / "Gestionador.py"
archivo_gestor = str(archivo_gestor)

with open(ruta, "r", encoding="utf-8") as archivo:
    ProtoGex = archivo.read()

# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
# IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

def ejecutar(entorno):

    try:
        Resultado = Gestionar(entorno)

        rcode = Resultado[0]

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

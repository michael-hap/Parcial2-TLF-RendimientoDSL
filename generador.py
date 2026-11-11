
import json
import sys

from pathlib import Path
from contextlib import redirect_stdout

from io import StringIO


class Nodo:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.hijos = []

    def agregar_hijos(self, simbolos):
        self.hijos = [Nodo(simbolo) for simbolo in simbolos]

    def es_hoja(self):
        return len(self.hijos) == 0

def cargar_gramatica(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    simbolo_inicial = datos["simbolo_inicial"]
    producciones = datos["producciones"]

    return simbolo_inicial, producciones


def cargar_ejemplo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)



def obtener_hojas(nodo):
    if nodo.es_hoja():
        return [nodo]

    hojas = []

    for hijo in nodo.hijos:
        hojas.extend(obtener_hojas(hijo))

    return hojas


def aplicar_produccion(raiz, producciones, alternativa, direccion):
    hojas = obtener_hojas(raiz)

    no_terminales = [
        hoja for hoja in hojas
        if hoja.simbolo in producciones
    ]

    if not no_terminales:
        raise ValueError("No quedan símbolos no terminales por expandir.")

    if direccion == "izquierda":
        nodo = no_terminales[0]
    elif direccion == "derecha":
        nodo = no_terminales[-1]
    else:
        raise ValueError("La dirección debe ser 'izquierda' o 'derecha'.")

    simbolo = nodo.simbolo

    if alternativa not in producciones[simbolo]:
        raise ValueError(
            f"La producción {simbolo} → {' '.join(alternativa)} no es válida."
        )

    nodo.agregar_hijos(alternativa)

    return simbolo


def mostrar_arbol(nodo, prefijo="", es_ultimo=True):
    if prefijo == "":
        print(nodo.simbolo)
    else:
        conector = "└── " if es_ultimo else "├── "
        print(prefijo + conector + nodo.simbolo)

    for indice, hijo in enumerate(nodo.hijos):
        ultimo_hijo = indice == len(nodo.hijos) - 1

        if prefijo == "":
            nuevo_prefijo = "    "
        else:
            nuevo_prefijo = prefijo + (
                "    " if es_ultimo else "│   "
            )

        mostrar_arbol(hijo, nuevo_prefijo, ultimo_hijo)


def validar_derivacion(raiz, producciones, cadena_esperada):
    hojas = obtener_hojas(raiz)

    pendientes = [
        hoja.simbolo
        for hoja in hojas
        if hoja.simbolo in producciones
    ]

    if pendientes:
        raise ValueError(
            "La derivación está incompleta. "
            f"No terminales pendientes: {pendientes}"
        )

    cadena_generada = [hoja.simbolo for hoja in hojas]

    if cadena_generada != cadena_esperada:
        raise ValueError(
            "La cadena generada no coincide con la esperada."
        )

    return cadena_generada


def guardar_resultado(ruta_salida, contenido):
    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

    print(f"\nResultado guardado en: {ruta}")



if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Uso: python generador.py <archivo_ejemplo.json>")
            sys.exit(1)

        simbolo_inicial, producciones = cargar_gramatica(
            "ejemplos/gramatica.json"
        )

        ejemplo = cargar_ejemplo(sys.argv[1])
        raiz = Nodo(simbolo_inicial)

        direccion = ejemplo["direccion"]
        pasos = ejemplo["pasos"]

        salida = StringIO()

        with redirect_stdout(salida):
            print("Ejemplo:", ejemplo["nombre"])
            print("Derivación:", direccion)
            print("\nAplicando producciones:\n")

            for numero, alternativa in enumerate(pasos, start=1):
                simbolo = aplicar_produccion(
                    raiz,
                    producciones,
                    alternativa,
                    direccion
                )

                print(
                    f"Paso {numero}: "
                    f"{simbolo} → {' '.join(alternativa)}"
                )

            cadena_generada = validar_derivacion(
                raiz,
                producciones,
                ejemplo["cadena_esperada"]
            )

            print("\nCadena generada:")
            print(" ".join(cadena_generada))

            print("\nVerificación:")
            print("CORRECTO: derivación completa y cadena verificada.")

            print("\nÁrbol de derivación:")
            mostrar_arbol(raiz)

        contenido = salida.getvalue()

        print(contenido)

        nombre_archivo = Path(sys.argv[1]).stem + ".txt"
        ruta_salida = Path("salidas") / nombre_archivo

        guardar_resultado(ruta_salida, contenido)

    except (ValueError, KeyError, FileNotFoundError, json.JSONDecodeError) as error:
        print(f"\nERROR: {error}")
        sys.exit(1)

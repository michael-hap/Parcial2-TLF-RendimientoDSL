
# RendimientoDSL - Segundo Parcial TLF

## Descripción

RendimientoDSL es un lenguaje específico de dominio (DSL)
diseñado para representar configuraciones de pruebas de
rendimiento mediante una Gramática Independiente del
Contexto (GIC).

El lenguaje permite describir escenarios, usuarios
virtuales, duración y métricas de rendimiento.

Este proyecto implementa en Python un generador de árboles
de derivación a partir de producciones gramaticales y
pasos de derivación proporcionados mediante archivos JSON.

El programa no implementa un parser ni ejecuta pruebas
reales de rendimiento.

## Tecnologías utilizadas

- Python 3.11.9
- JSON
- Visual Studio Code
- Git y GitHub

No se requieren bibliotecas externas.

## Estructura del proyecto

```text
Parcial2-TLF-RendimientoDSL/
├── generador.py
├── ejemplos/
│   ├── gramatica.json
│   ├── w1_izquierda.json
│   ├── w2_derecha.json
│   └── prueba_incompleta.json
├── salidas/
│   ├── w1_izquierda.txt
│   └── w2_derecha.txt
├── README.md
└── .gitignore
```

## Gramática implementada

La gramática se define mediante:

G = (V, Σ, R, S)

Donde:

- V: conjunto de símbolos no terminales.
- Σ: conjunto de símbolos terminales.
- R: reglas de producción.
- S: símbolo inicial.

Las producciones se encuentran almacenadas en
`ejemplos/gramatica.json`.

La gramática incluye recursividad por la derecha para
representar múltiples escenarios y múltiples métricas.

## Ejemplo de RendimientoDSL

```text
escenario login {
    usuarios 100;
    duracion 60;
    metrica latencia;
}
```

## Instrucciones de ejecución

### 1. Requisitos

Tener instalado Python 3.11 o superior.

### 2. Abrir una terminal

Ubicarse en la carpeta principal del proyecto.

### 3. Ejecutar la derivación por izquierda

```bash
python generador.py ejemplos/w1_izquierda.json
```

### 4. Ejecutar la derivación por derecha

```bash
python generador.py ejemplos/w2_derecha.json
```

## Ejemplos implementados

### Ejemplo 1: derivación por izquierda

Escenario: login.

- Usuarios virtuales: 100.
- Duración: 60 segundos.
- Métrica: latencia.
- Producciones aplicadas: 10.

### Ejemplo 2: derivación por derecha

Escenario: compra.

- Usuarios virtuales: 50.
- Duración: 120 segundos.
- Métricas: errores y throughput.
- Producciones aplicadas: 12.

La segunda derivación demuestra el uso de recursividad
en la lista de métricas.

## Validaciones implementadas

El generador comprueba:

- Que la producción seleccionada exista en la gramática.
- Que se expanda el no terminal correspondiente
  según la dirección de derivación.
- Que no queden símbolos no terminales sin desarrollar.
- Que la cadena generada coincida con la cadena esperada.

### Prueba de derivación incompleta

```bash
python generador.py ejemplos/prueba_incompleta.json
```

El programa detecta que faltan símbolos no terminales
por desarrollar y muestra un mensaje de error.

## Resultados

Cada ejecución válida genera:

1. Secuencia de producciones aplicadas.
2. Cadena terminal resultante.
3. Mensaje de verificación.
4. Árbol de derivación jerárquico.

Los resultados también se guardan automáticamente
en la carpeta `salidas/`.

## Relación con el informe

Las derivaciones implementadas corresponden a las
cadenas w1 y w2 desarrolladas en la Sección III
del informe técnico.

Los árboles generados conservan la misma estructura
que los árboles presentados manualmente.

## Autor

Michael Hernan Acevedo Porras

## Asignatura

Teoría de Lenguajes Formales.

Programa de Ingeniería de Sistemas y Computación.

Segundo Parcial - Noviembre de 2026.

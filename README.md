# Analizador Léxico - FLEX + Python (MiniLang)

Este proyecto implementa un **Analizador Léxico (Scanner)** para un subconjunto simplificado de un lenguaje de programación denominado **MiniLang**. Combina la velocidad nativa de un motor léxico escrito en **Flex (C)** con una interfaz gráfica amigable de usuario desarrollada en **Python (Tkinter)** bajo un tema oscuro moderno.

Este proyecto ha sido desarrollado como una asignación práctica para la materia de Compiladores / Teoría de Lenguajes por un estudiante de Ingeniería de Sistemas.

## 🚀 Características

- **Motor Léxico en C (Generado por Flex):** Clasificación extremadamente rápida y óptima de tokens.
- **Interfaz Gráfica Moderna (Tkinter):** Tematización oscura personalizada sin consola, con paneles divididos y barra de estado.
- **Tabla de Tokens Estructurada:** Visualización interactiva mediante cuadrícula (`Treeview`) que categoriza cada token (Palabras clave, Operadores, Números, Identificadores, etc.).
- **Consola de Salida Raw:** Permite visualizar el flujo puro de tokens devuelto por el analizador ejecutable.
- **Plantillas de Código:** Selector rápido para cargar ejemplos típicos (bucle simple, condicional if-else, operaciones aritméticas).
- **Exportación:** Posibilidad de guardar los resultados del análisis en un archivo CSV.

---

## 🛠️ Requisitos de Instalación y Construcción

Para compilar y ejecutar este proyecto en Windows, se requiere tener instalados:

1. **Flex & GCC (MinGW-w64):** Se pueden obtener instalando la suite MinGW o herramientas como `winflexbison`. Asegúrate de que estén agregados al `PATH` del sistema.
2. **Python 3.10+** (incluye `tkinter` por defecto en Windows).

---

## 📦 Instrucciones de Compilación y Ejecución

El proyecto incluye un script de automatización (`build.bat`) para compilar de forma limpia.

### Paso 1: Compilar el Analizador Léxico (Flex a C, C a EXE)
Abre una terminal en este directorio y ejecuta:
```bash
build.bat
```
Esto generará los siguientes archivos:
- `lex.yy.c`: Código fuente en C producido por Flex.
- `lexer.exe`: Ejecutable final optimizado para el análisis de tokens.

### Paso 2: Lanzar la Aplicación Gráfica
Ejecuta la interfaz en Python con:
```bash
python gui_app.py
```

---

## 📘 Especificación del Lenguaje (MiniLang)

El analizador léxico procesa los siguientes patrones y los agrupa en categorías:

| Componente Léxico | Expresión Regular | Token Producido | Ejemplo |
| :--- | :--- | :--- | :--- |
| **Palabra Clave `if`** | `if` | `TOKEN_IF` | `if` |
| **Palabra Clave `else`** | `else` | `TOKEN_ELSE` | `else` |
| **Palabra Clave `while`** | `while` | `TOKEN_WHILE` | `while` |
| **Palabra Clave `return`** | `return` | `TOKEN_RETURN` | `return` |
| **Identificadores** | `[a-zA-Z_][a-zA-Z0-9_]*` | `TOKEN_ID` | `contador`, `x`, `_temp` |
| **Números Enteros** | `[0-9]+` | `TOKEN_NUM` | `42`, `0`, `999` |
| **Operadores** | `[+\-*/]` | `TOKEN_OP` | `+`, `-`, `*`, `/` |
| **Espacios / Saltos** | `[ \t\r\n]+` | *(Ignorados)* | Espacios, tabs, saltos de línea |
| **Error / Desconocido**| `.` (cualquier otro) | `TOKEN_UNKNOWN` | `$`, `@`, `#` |

---

## 🎨 Explicación del Autómata (DFA)

El comportamiento interno del analizador léxico está regido por un **Autómata Finito Determinista (AFD)** o DFA. 

### Diagrama de Transición Conceptual

```
                  [a-zA-Z_]
               +------------+
               |            |
               v            |
        +---------------+   |
        |  S1: Identif. |---+  (Aceptación / Clasifica palabras clave)
        +---------------+
          ^
          | [a-zA-Z_]
          |
     ( Estado S0 ) --- [0-9] ---> +---------------+
       (Inicio)                   |  S2: Número   |---+ [0-9]
          |                       +---------------+   |
          |                               ^           |
          | [+\-*/]                       +-----------+
          v
     +------------+
     |S3: Operador| (Aceptación)
     +------------+
          |
          | Caracter no válido
          v
     +------------+
     |  S4: Error | (Aceptación de token desconocido)
     +------------+
```

### Explicación de Estados del AFD:
1. **Estado S0 (Inicio):** Lee el primer carácter de la cadena.
   - Si es una letra (`a-z`, `A-Z`) o un guion bajo (`_`), transita al **Estado S1** (acumulador de identificador).
   - Si es un dígito (`0-9`), transita al **Estado S2** (acumulador de constante numérica).
   - Si es un operador aritmético (`+`, `-`, `*`, `/`), transita al **Estado S3** y acepta el token inmediatamente.
   - Si es un espacio en blanco (` `, `\t`, `\n`), se descarta y vuelve a **S0**.
   - Si es cualquier otro carácter, transita a **S4** y reporta un token desconocido.
2. **Estado S1 (Identificador):** Permanece consumiendo letras y dígitos. Al encontrar un delimitador u operador, se detiene y realiza una búsqueda semántica para verificar si el lexema acumulado es una palabra clave (`if`, `else`, `while`, `return`). Si no lo es, lo clasifica como identificador (`TOKEN_ID`).
3. **Estado S2 (Constante Numérica):** Permanece consumiendo dígitos (`0-9`). Al encontrar una letra o delimitador, se detiene y clasifica el lexema como `TOKEN_NUM`.
4. **Estado S3 (Operadores):** Estado de aceptación simple para operadores de un único carácter.
5. **Estado S4 (Error):** Estado de aceptación para manejar caracteres que no pertenecen a la gramática de MiniLang.

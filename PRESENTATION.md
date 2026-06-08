# Guía de Presentación para la Clase: Analizador Léxico con FLEX y Python

Esta guía contiene la estructura de diapositivas recomendada, los puntos de explicación teórica y el guion sugerido para tu presentación ante el docente y la clase.

---

## 📊 Estructura de Diapositivas Sugerida

### Diapositiva 1: Portada
- **Título:** Diseño e Implementación de un Analizador Léxico con FLEX y Python
- **Subtítulo:** Integración de herramientas nativas de compilación y desarrollo de interfaces de usuario modernas.
- **Presentador:** [Tu Nombre] - Ingeniería de Sistemas

### Diapositiva 2: ¿Qué es el Análisis Léxico?
- **Puntos clave:**
  - El análisis léxico es la **primera fase** de un compilador.
  - Su objetivo es leer el código fuente carácter por carácter y agruparlos en unidades con significado lógico llamadas **Lexemas**.
  - Asocia a cada lexema una categoría conocida como **Token**.
  - Descarta elementos innecesarios como comentarios y espacios en blanco.

### Diapositiva 3: Arquitectura Híbrida del Proyecto
- **Puntos clave:**
  - **Motor Léxico (FLEX en C):** Proporciona la velocidad de ejecución y robustez matemática de los autómatas finitos.
  - **Interfaz de Usuario (Python + Tkinter):** Ofrece una aplicación interactiva, moderna y con tema oscuro para evitar el uso directo de consola.
  - **Mecanismo de comunicación:** Python escribe el código temporalmente en un archivo de entrada, invoca a `lexer.exe` en un subproceso de fondo enviándole dicho archivo, y lee su flujo de salida estándar (`stdout`) para formatearlo en una tabla interactiva en tiempo real.

---

## 🎨 Explicación del Autómata Finito Determinista (AFD)

Esta sección es crucial para tu presentación. Explica cómo la teoría de compiladores se plasma en el código.

### Tabla de Transición de Estados

| Estado Actual | Carácter Leído | Siguiente Estado | Acción / Token Producido |
| :--- | :--- | :--- | :--- |
| **S0 (Inicio)** | Letra (`a-z`, `A-Z`) o `_` | **S1** | Acumula lexema |
| **S0 (Inicio)** | Dígito (`0-9`) | **S2** | Acumula lexema numérico |
| **S0 (Inicio)** | Operador (`+`, `-`, `*`, `/`) | **S3 (Aceptación)** | Emite `TOKEN_OP` inmediatamente |
| **S0 (Inicio)** | Espacio en blanco (` `, `\t`, `\n`) | **S0** | Descarta carácter |
| **S0 (Inicio)** | Cualquier otro carácter | **S4 (Aceptación)** | Emite `TOKEN_UNKNOWN` |
| **S1 (Identif.)** | Letra, Dígito o `_` | **S1** | Sigue acumulando |
| **S1 (Identif.)** | Delimitador u Operador (otro) | **Aceptación (Retorno)** | Verifica si es palabra clave (`if`, `else`, etc.) o `TOKEN_ID` |
| **S2 (Número)** | Dígito (`0-9`) | **S2** | Sigue acumulando |
| **S2 (Número)** | No Dígito | **Aceptación (Retorno)** | Emite `TOKEN_NUM` |

### Puntos clave para explicar ante la clase:
1. **La coincidencia del prefijo más largo (Longest Match Rule):** FLEX consume caracteres mientras cumplan con la regla. Por ejemplo, en `if_value`, FLEX no se detiene en `if`, sino que consume todo el texto porque coincide con un identificador válido que es más largo.
2. **Prioridad de Reglas:** Si dos reglas coinciden con la misma cantidad de caracteres (como en la palabra `if` que encaja tanto en la regla de palabra clave `if` como en la de identificador `{ID}`), FLEX selecciona la regla que aparece **primero** en el archivo `.l`. Por eso las palabras clave están definidas antes que los identificadores genéricos.

---

## 💻 Guía de Funcionamiento del Código

### 1. El motor FLEX (`lexer.l`)
- **Sección de definiciones:** Define macros simples como `DIGIT [0-9]+` e `ID [a-zA-Z_][a-zA-Z0-9_]*`.
- **Sección de reglas:** El emparejamiento usa expresiones regulares.
- **`%option noyywrap`:** Indica que el analizador no requiere procesar múltiples archivos fuente consecutivamente, lo que simplifica la compilación en Windows sin necesitar bibliotecas adicionales.

### 2. La interfaz en Python (`gui_app.py`)
- Utiliza la biblioteca estándar `tkinter` junto con `ttk` para crear la interfaz visual.
- El método `run_lexer` escribe el contenido actual del editor de texto en un archivo de entrada temporal (`tmp_input.txt`).
- Invoca al ejecutable compilado mediante la función:
  ```python
  subprocess.run([LEXER_EXE], input=open(temp_path, "rb").read(), capture_output=True)
  ```
- **Procesamiento de salida:** Divide el string resultante por saltos de línea y clasifica los tokens en un widget de tipo tabla (`ttk.Treeview`), asignando categorías descriptivas para el usuario final.

---

## 🎤 Guion Sugerido (Paso a Paso)

1. **Introducción:** *"Buenos días, profesor y compañeros. Hoy les presentaré un analizador léxico desarrollado en un enfoque híbrido, combinando el poder y eficiencia del generador Flex en C con una interfaz moderna y amigable en Python..."*
2. **Teoría del AFD:** *"El núcleo de nuestro analizador se modela mediante un Autómata Finito Determinista. Como pueden ver en la tabla de transición, empezamos en el estado S0. Si leemos una letra, el autómata transita al estado S1..."*
3. **Demostración Práctica:** *[Abre la aplicación gráfica]* *"La aplicación cuenta con varias plantillas preestablecidas. Por ejemplo, si cargamos la plantilla de 'Condición If-Else' y presionamos 'Analizar Código', vemos de forma estructurada en la tabla cada uno de los tokens detectados con su categoría..."*
4. **Conclusión:** *"Este proyecto demuestra cómo la teoría abstracta de los compiladores puede implementarse con herramientas clásicas del estándar POSIX e integrarse con lenguajes modernos de desarrollo rápido como Python para crear herramientas interactivas."*

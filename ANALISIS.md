# Análisis — Tarea 1

**Integrantes:**
1. Correa Merino Fernanda
2. Pérez Hernández Francisco Gadiel

**Fork: https://github.com/fujonanda/tarea1-mini-interprete.git**
**Rama: tarea1-pruebas-refactorizacion**

---

## 1. Arquitectura

### 1.1 ¿Cuál es la responsabilidad de cada componente?

| Componente | Qué recibe | Qué entrega | De qué es responsable |
|---|---|---|---|
| `lexer` |Secuencia de caracteres del código fuente|Unidades con significado (tokens)|Convertir caracteres en tokens con un significado que la computadora pueda entender|
| `parser` |Secuencia de tokens|Representación estructurada de la relación entre los tokens|Definir cómo pueden relacionarse los tokens entre sí considerando las reglas gramáticales|
| `ast` |Datos obtenidos del parser|Estructura que representa la jerarquía de los tokens|Representar las operaciones y la jerarquía de los tokens presentes en el programa|
| `evaluator` |La representación de las operaciones hechas a los tokens|El resultado de evaluar las operaciones|Determinar si la operación puede producir un resultado o si se trata de un error|

### 1.2 ¿Qué recorrido sigue una expresión desde que se recibe como texto hasta que produce un resultado?
Primero pasa por el lexer que se encarga de separar la expresión en tokens con significado para la computadora, los tokens pasan al parser donde se usan las reglas gramáticales definidas por el lenguaje para crear una representación del orden que llevan las operaciones, dicha representación puede tratarse de un AST, después el evaluator analiza la estructura de la representación creada y determina si la operación es correcta para producir su resultado, en caso de ser incorrecta la marca como un error

> Usen `(3 + 4) * 2` como ejemplo y muestren cómo se ve entre etapa y etapa.

| Etapa | Cómo se ve `(3 + 4) * 2` aquí |
|---|---|
| texto | `"(3 + 4) * 2"` |
| tokens | [Token(PAR_IZQ, "(", 0), Token(NUMERO, 3, 1), Token(MAS, "+", 3), Token(NUMERO, 4, 5), Token(PAR_DER, ")", 6), Token (POR, "*", 8), Token(NUMERO, 2, 10)] |
| AST | Raíz: [Operador "*"] Nivel 1: [Número 2] [Operador "+"] Nivel 2: [Número 3] [Número 4] |
| resultado | 14 |

El AST dibujado por el equipo antes de hacer la prueba coincidió con el dibujo del árbol realizado por el programa
---

## 2. Las pruebas que ya estaban

### 2.1 ¿Qué pruebas venían incluidas?

| Prueba | Componente | Comportamiento que verifica | ¿Cuántos operadores usa? | ¿Normal, frontera o inválida? |
|---|---|---|---|---|
| `test_suma` | Evaluator | Calcular bien la suma de 2 enteros. | 1 (`+`) | Normal |
| `test_resta` | Evaluator | Calcular bien la resta de 2 enteros. | 1 (`-`) | Normal |
| `test_multiplicacion` | Evaluator | Calcular correctamente el producto/multiplicación de 2 enteros. | 1 (`*`) | Normal |
| `test_division` | Evaluator | Calcular correctamnete la división de 2 enteros. | 1 (`/`) | Normal |
| `test_precedencia_sin_parentesis` | Evaluator | El resultado respetando la jerarquía con base a la precedencia implícita. | 2 (`+`, `*`) | Normal |
| `test_precedencia_con_parentesis` | Evaluator | El resultado alterando la prioridad jerárquica con paréntesis. | 2 (`+`, `*`) | Normal |
| `test_tokeniza_un_numero_solo` | Lexer | "Tokenización" de un número entero a... un token | 0 | Normal |
| `test_tokeniza_una_suma` | Lexer | Reconocimiento de operandos y operador binario, así como su secuencia correcta de ejecución. | 1 (`+`) | Normal |
| `test_los_espacios_no_producen_tokens` | Lexer | Descarta la existencia de cualquier espacio blanco para no hacerlo token.| 1 (`+`) | Frontera |
| `test_tokeniza_parentesis` | Lexer | Denota a los paréntesis/símbolos de agrupación para la cohesión estructural. | 0 | Normal |
| `test_construye_el_arbol_de_una_suma` | Parser | Construcción de un AST de un solo nivel para representar la suma (como que el nombre del test es muy explicatorio per se, para todos). | 1 (`+`) | Normal |
| `test_la_multiplicacion_se_agrupa_antes_que_la_suma` | Parser | Anidar a los nodos propiamente priorizand la multiplicación (racismo de operandos). | 2 (`+`, `*`) | Normal |
| `test_los_parentesis_cambian_la_agrupacion` | Parser | Anidar a los nodos con base a los paréntesis. | 2 (`+`, `*`) | Normal |

### 2.2 ¿Qué comportamientos **no** estaban probados?

Para lexer:
1. Reconocer a números de varios dígitos y a símbolos como tokens
2. Responder correctamente a las operaciones sin importar los espacios y saltos de línea que se ingresen
3. Manejar el caso en el que se ingrese un caracter con el que el programa no pueda trabajar
4. Manejar el caso en el que se ingresen letras junto a los números

Para parser:
1. Colocar el operador "*" (multiplicación) en un nivel inferior al operador "+" (suma) en el AST
2. Realizar las operaciones con resta en orden de izquierda a derecha cuando no hay paréntesis ni operaciones de mayor jerarquía
3. Realizar las operaciones con división en orden de izquierda a derecha cuando no hay paréntesis ni operaciones de menor jerarquía
4. Manejar el caso en el que un paréntesis no se cierre correctamente
5. Manejar el caso en el que se ingrese una operación que no contenga ningún operador

Para evaluator:
1. Realizar operaciones corretamente que contengan paréntesis dentro de otros paréntesis
2. Realizar correctamente las operaciones que involucren tres números
3. Realizar correctamente operaciones donde haya dos operandos involucrados
4. Manejar en caso en el que se haga una división cualquiera con el 0 como divisor
5. Manejar el caso en el que se intenten realizar operaciones con números negativos
6. Producir un resultado flotante para las divisiones
7. Realizar operaciones binarias en un AST de forma correcta
8. Producir un resultado negativo para una resta cuando sea el caso
9. Rechazar símbolos que no representen números ni operandos en un AST
10. Manejar el caso en el que se intente dividir un número entre 0 en un árbol binario

---

## 3. Las pruebas que agregaron

### 3.1 ¿Cuáles son casos normales, cuáles frontera y cuáles inválidos?

| Prueba (archivo::nombre) | Entrada | Esperado | Categoría | ¿Por qué esa categoría? |
|---|---|---|---|---|
| | | | | |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

> No basta con "daba mal". Digan contra qué lo están comparando: qué regla,
> qué línea de la semántica declarada del README.

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| | | | | | |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

---

## 5. Diseño

### 5.1 ¿Qué duplicación o señal de mal diseño encontraron?

> Al menos dos. Usen el vocabulario de clase: duplicación, rigidez,
> acoplamiento alto, condicionales repetidos, amplificación del cambio.

### 5.2 ¿Qué refactorización realizaron, y por qué conserva el comportamiento?

> "Las pruebas siguen pasando" es parte de la respuesta, pero no toda.
> ¿Por qué el cambio es equivalente?

### 5.3 ¿Sería pertinente usar Factory Method, Adapter o ninguno?

> Justifiquen. **"Ninguno" puede ser la respuesta correcta.** Si dicen que sí,
> digan qué problema concreto resuelve y qué costo tiene. Si dicen que no,
> digan qué tendría que cambiar en el sistema para que empezara a convenir.

### 5.4 ¿Qué parte del sistema sería más difícil de modificar si se agregara un operador nuevo?

> Por ejemplo `%`. ¿Cuántos archivos hay que tocar? ¿Por qué?

---

## Antes de la declaración: inténtenlo primero ustedes

Usar IA o no es decisión de cada quien, y el curso la permite. Pero **les
pedimos, por favor, que primero hagan el análisis por su cuenta.**

No es una prueba de honestidad. Es que el orden cambia lo que aprenden:

1. **Primero ustedes.** Lean el código, corran las pruebas, escriban sus
   respuestas. Aunque queden incompletas, aunque no encuentren todo.

2. **Después, si quieren, la IA** — pero como contraste, no como sustituto.
   Y entonces contesten dos preguntas, en `DECLARACION_IA.md`:

   - **¿Qué encontró que ustedes no habían notado?**
     Eso es aprendizaje, y se declara sin ninguna pena.

   - **¿Qué *no* encontró, que en este curso sí consideramos un problema?**
     Ésta es la interesante. Una herramienta suele decir que el código
     "funciona bien" y no señalar, por ejemplo, la **duplicación** — porque
     duplicar no rompe nada, el programa corre igual. Pero ustedes ya saben
     por qué eso sí es un mal diseño, y saben nombrarlo. La herramienta no
     tomó esa clase.

> Si invierten el orden se pierden justamente lo segundo: **no se puede notar
> lo que a una herramienta le faltó si uno nunca se formó una opinión propia
> antes de preguntarle.** Y que un programa funcione no implica que esté bien
> diseñado — eso lo dijimos en clase mucho antes de esta tarea.

---

## Declaración de uso de Inteligencia Artificial

Va en `DECLARACION_IA.md`, no aquí. Es obligatoria, pero **no da ni quita
puntos**: es un reporte adicional que se revisa aparte y se les devuelve con
comentarios.

**No se evalúa cuánta IA usaron.** Se evalúa si pueden dar cuenta de lo que
entregaron. *"No usamos"* es una declaración válida y completa; *"lo
descartamos porque..."* es de las mejores respuestas posibles.

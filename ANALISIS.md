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
| `test_reconocer_operacion_basica` | "13 + 3" | [Token(TipoToken.NUMERO, 13, 0), Token(TipoToken.MAS, "+", 3), Token(TipoToken.NUMERO, 3, 5)] | Normal | Es una operación que se realiza de forma común sin entradas que necesiten manejarse de forma particular |
| `test_respuesta_a_espaciado_irregular` | "  45   \n * \t 2 " | [Token(TipoToken.NUMERO, 45, 2), Token(TipoToken.POR, "*", 10), Token(TipoToken.NUMERO, 2, 14)] | Frontera | Incluye espacios y saltos de línea que no se espera que se ingresen como entrada pero con los que el programa aún es capaz de producir una respuesta |
| `test_caracter_desconocido_invalido` | "6 $ 9" | ErrorDeSintaxis | Inválido | El caracter "$" no está definido como un comando del intérprete entonces no se considera como una entrada válida |
| `test_letras_vocabulario_invalido` | "10a + 5" | ErrorDeSintaxis | Inválido | El programa solo trabaja con números constantes y operandos, añadir letras no produce resultados |
| `test_multiplicacion_abajo_de_la_suma` | "7 + 5 * 10" | Parser(tokenizar(entrada)).parsear() | Normal | Es una operación que se realiza de forma común y que el programa puede manejar fácilmente |
| `test_orden_izquierda_a_derecha_division` | "36 / 6 / 3" | OperacionBinaria("/", OperacionBinaria("/", Numero(36), Numero(6)), Numero(3)) | Frontera | La operación debe realizarse en un orden específico, de lo contrario producirá un resultado erróneo |
| `test_falta_parentesis` | "(24 - 27" | ErrorDeSintaxis, match="se esperaba ')'" | Inválido | Todos los paréntesis abiertos durante una operación deben cerrarse para que esta pueda llevarse a cabo |
| `test_falta_operador` | "2 12" | ErrorDeSintaxis | Inválido | Una operación sin un operador definido no puede realizarse |
| `test_parentesis_dentro_de_parentesis_1` | "(21 - (4 / 2)) * 3" | 57.0 | Normal | Es una operación con valores y operaciones comunes cuyo orden está bien definido por paréntesis |
| `test_parentesis_dentro_de_parentesis_2` | "6 + ((7 / 2) * 8)" | 34.0 | Normal | Define un caso casi idéntico al anterior con un sencillo cambio de orden |
| `test_suma_de_tres` | "10 + 4 + 3" | 17 | Frontera | Se prueba el orden en el que se ejecuta la operación de la suma para más de dos números sin distintas jerarquías ni paréntesis |
| `test_resta_de_tres` | "10 - 5 - 3" | 2 | Frontera | Se prueba lo mismo que en el caso anterior, esta vez es más importante ya que la resta es suceptible a arrojar resultados distintos al cambiar el orden de la misma operación |
| `test_multiplicacion_de_tres` | "6 * 3 * 2" | 36 | Frontera | Comprueba el orden para el caso de la multiplicación |
| `test_division_de_tres` | "50 / 2 / 5" | 5.0 | Frontera | Comprueba el orden para el caso de la división que, del mismo modo que la resta, se ve afectada por cambios de orden |
| `test_suma_y_resta` | "20 + 10 - 8" | 22 | Frontera | Pone a prueba el orden para dos operaciones distintas de la misma jerarquía (suma y resta) |
| `test_resta_y_suma` | "7 - 4 + 2" | 5 | Frontera | Prueba lo mismo que el caso anterior, siendo ahora una de ellas afectada por el orden de la operación |
| `test_multiplicacion_y_division` | "4 * 20 / 5" | 16.0 | Frontera | Prueba el orden para una operación que involucra una multiplicación y una división, las cuales se encuentran en la misma jerarquía, sin uso de paréntesis |
| `test_division_y_multiplicacion` | "36 / 3 * 2" | 24.0 | Frontera | Hace la misma prueba que el caso anterior con la resta siendo afectada por cambios en el orden de la operación |
| `test_division_entre_cero` | "10 / 0" | ErrorDeEvaluacion, match="division entre cero" | Frontera | La división sobre 0 se encuentra definida a pesar de que se pueda usar para hacer más operaciones como un número válido |
| `test_suma_con_negativos` | "-3 + -4" | ErrorDeSintaxis | Inválido | El programa no soporta números con signo fuera del definido por el operador |
| `test_resta_con_negativos` | "-10 - -7" | ErrorDeSintaxis | Inválido | No se pueden ingresar números con signo al programa |
| `test_multiplicacion_con_negativos` | "-5 * -9" | ErrorDeSintaxis | Inválido | El programa solo permite números representados con su valor absoluto |
| `test_division_con_negativos` | "-16 / -8" | ErrorDeSintaxis | Inválido | No se admiten números con signo para las operaciones del programa |
| `test_suma_basica_en_AST` | OperacionBinaria("+", Numero(6), Numero(7)) | 13 | Normal | Plantea una operación binaria sencilla usando el operador "+" con números comunes y admitidos por el programa |
| `test_resta_basica_en_AST` | OperacionBinaria("-", Numero(9), Numero(3)) | 6 | Normal | Define una operación con "-" y números fácilmente manejables |
| `test_producto_basico_en_AST` | OperacionBinaria("*", Numero(9), Numero(11)) | 99 | Normal | Realiza una operación con el operador "*" y números con los que el programa puede trabajar cómodamente |
| `test_division_valida_con_float_decimal` | OperacionBinaria("/", Numero(13), Numero(2)) | 6.5 | Normal | Prueba realizar una división sencilla y su capacidad para producir resultados de tipo flotante |
| `test_resta_con_resultado_negativo` | OperacionBinaria("-", Numero(9), Numero(11)) | -2 | Frontera | Comprueba que una resta puede generar resultados negativos si se da el caso |
| `test_operador_desconocido_invalido` | OperacionBinaria("^", Numero(6), Numero(7)) | ErrorDeEvaluacion | Inválido | No se pueden ingresar caracteres distintos a los operadores y números con los que trabaja el programa |
| `test_nodo_desconocido` | "Salu2 bella profesora o bello profesor. Este nodo debe fallar al no ser uno del AST, solo un string" | ErrorDeEvaluacion | Inválido | Un nodo no puede contener un dato distinto a un número o uno de los operadores definidos por el programa |
| `test_division_por_cero_en_AST` | OperacionBinaria("/", Numero(93), Numero(0)) | ErrorDeEvaluacion, match="division entre cero" | Inválido | La división entre 0 es indefinida y no puede producir un resultado que se pueda representar con el intérprete |

---

## 4. Los defectos

### 4.1 ¿Qué defecto reveló primero una prueba nueva?
Las operaciones que involucraban operaciones de la misma jerarquía y que no usaban paréntesis para definir un orden se resolvían comenzando por la derecha y terminando por la izquierda, lo que provocó que en operaciones con restas o divisiones de por medio el resultado fuera erróneo. Lo mismo ocurría para las operaciones binarias con los AST.
A su vez, el programa no lanzaba los errores definidos para el caso en el que se ingresaran números junto con letras, se ingresaba un caracter desconocido el programa o no se agregara ningún operador a la operación.
Para el caso en el que no se cerraba un paréntesis que ya se había abierto el programa lanzaba IndexError

### 4.2 ¿Por qué el comportamiento observado era incorrecto?

- Línea 6 de la semántica: Indica que en caso de tener una operación con operadores de la misma precedencia estos deben asociarse a la izquierda, cosa que no pasó y es por eso que las operaciones de este tipo que involucraban operadores sensibles a los cambios de orden generaran resultados erróneos
- Línea 8 de la semántica: Indica que las entradas erróneas deben rechazarse con ErrorDeSintaxis en lugar de errores propios de Python, esto no sucedía cuando se ingresaban caracteres que no se encontraban definidos en los comandos del intérprete o en su defecto cuando a una operación le faltaban tokens para considerarse válida

### 4.3 ¿Qué cambio realizaron?

| Defecto | Entrada que lo revela | Daba | Debería dar | Commit rojo | Commit verde |
|---|---|---|---|---|---|
| Las restas de más de tres números se asociaban hacia la derecha | "10 - 5 - 3" | 8 | 2 | 15a38d6 | b9833f8 |
| Las divisiones de más de tres números se asociaban a la derecha | "50 / 2 / 5" | 125.0 | 5.0 | 15a38d6 | b9833f8 |
| Las operaciones binarias se asociaban de derecha a izquierda | "36 / 6 / 3" | OperacionBinaria("/", OperacionBinaria("/", Numero(6), Numero(3)), Numero(36)) | OperacionBinaria("/", OperacionBinaria("/", Numero(36), Numero(6)), Numero(3)) | 14853c0 | b9833f8 |
| Ingresar un caracter desconocido no lanzaba ErrorDeSintaxis | "6 $ 9" | No marcaba ningún errorErrorDeSintaxis | ErrorDeSintaxis | 87c06dd | 937e8d6 |
| Ingresar números acompañados de letras no lanzaba ErrorDeSintaxis | "10a + 5" | No marcaba ningún errorErrorDeSintaxis | ErrorDeSintaxis | 87c06dd | 937e8d6 |
| La falta del cierre de un paréntesis lanzaba IndexError | "(24 - 27" | IndexError | ErrorDeSintaxis | 14853c0 | b9833f8 |
| La falta de operador en una operación no lanzaba ErrorDeSintaxis | "2 12" | No marcaba ningún errorErrorDeSintaxis | ErrorDeSintaxis | 14853c0 | b9833f8 |

### 4.4 ¿Cómo saben que la corrección es general y no sólo hace pasar ese ejemplo?

Se cambió el funcionamiento general del programa no solo para adecuarse al alcance de las nuevas pruebas que se definieron, sino a cualquier otro caso que pudiera presentarse. En el parser se cambió la forma en la que se asocian las operaciones para que, sin importar de cuántos números y operadores conste, siempre se iniciará su resolución por la izquierda y se terminará por la derecha. Por su parte se definió en el lexer que se lance un ErrorDeSintaxis cada vez que aparezca un símbolo o caracter no definido como token válido para el intérprete

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

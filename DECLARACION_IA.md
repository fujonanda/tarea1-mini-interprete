# Declaración de uso de Inteligencia Artificial

**Actividad: Tarea 1**
**Integrantes: Correa Merino Fernanda, Pérez Hernández Francisco Gadiel**
**Fecha: 19 de octubre de 2026**

> Esta declaración es obligatoria en toda tarea, práctica y en el proyecto final.
> **No da ni quita puntos**: es un reporte adicional que se revisa aparte y se
> devuelve con comentarios. **No se evalúa cuánta IA usaron**, sino si pueden
> dar cuenta de lo que entregaron.

---

## 0. ¿Se usó IA en esta actividad?

- [ ] **No.** Firmen la última sección y terminen. Con eso queda completa.
- [✓] **Sí.** Contesten los cinco puntos.

---

## 1. Herramienta(s) utilizada(s)

| Herramienta | Versión o modelo, si lo saben |
|---|---|
| Google Gemini | 3.1 Pro |

---

## 2. Objetivo del uso

| Para qué la usamos | En qué parte del entregable |
|---|---|
| Asistencia con git | La creación y modificaciones del repositorio donde se encuentra el entregable |
| Clasificación de las nuevas pruebas propuestas (casos normales, fronteras e inválidos) | En la documentación y organización de las pruebas dentro de los archivos test |

---

## 3. Prompts principales

Textuales, tal como los escribieron. No los limpien ni los reescriban.

```
creé un fork de un repositorio dado por un externo, se me ha dado la indicación de no trabajar sobre la rama Main y que debo crear una para los cambios que yo haga y después hacer un pull request titulado Tarea 1 — Apellido1, Apellido2, Apellido3, el nombre de la rama en la que trabaje debe ser el mismo que este título?
```

```
Cómo se define un caso frontera para el evaluator? Qué es la frontera en este caso, porque no es que los números se salgan del rango
```

```
Cómo verifico que en mi definición sí se haya contemplado a los negativos? Porque si no está bien definido, puede ser inválido, no?
```

```
def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("10 / 0") #Caso frontera

ESta es la defensa adjunta para este caso. Qué opinas?
```

```
Pero hace unos cuantos instantes me comentaste que ese era un caso inválido, NO frontera
```

```
# Casos frontera para las operaciones   
def test_suma_de_tres():
    assert interpretar("10 + 4 + 3") == 17

def test_resta_de_tres():
    # Este falla :p
    assert interpretar("10 - 5 - 3") == 2

def test_multiplicacion_de_tres():
    assert interpretar("6 * 3 * 2") == 36

def test_division_de_tres():
    # falla
    assert interpretar("50 / 2 / 5") == 5

def test_suma_y_resta():
    assert interpretar("20 + 10 - 8") == 22

def test_resta_y_suma():
    # falla
    assert interpretar("7 - 4 + 2") == 5

def test_multiplicacion_y_division():
    assert interpretar("4 * 20 / 5") == 16

def test_division_y_multiplicacion():
    # falla
    assert interpretar("36 / 3 * 2") == 24

def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion, match="division entre cero"):
        interpretar("10 / 0")


# Casos inválidos para operaciones

def test_suma_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3 + -4")

def test_resta_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-10 - -7")

def test_multiplicacion_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-5 * -9")

def test_division_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-16 / -8")


Reanalízame estos casos ahora entonces por favor, no me esperaba tan súbito cambio de perspectiva
```

```
def test_division_por_cero_lanza_error_de_evaluacion():
    """Verifica que dividir entre cero lance un ErrorDeEvaluacion."""
    with pytest.raises(ErrorDeEvaluacion):
        interpretar("10 / 0")

Misma a la anterior pero esta defensa presenta que es inválida. Cuál es el veredicto?
```

```
def test_suma_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-3 + -4")

def test_resta_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-10 - -7")

def test_multiplicacion_con_negativos():
    with pytest.raises(ErrorDeSintaxis):
        interpretar("-5 * -9")

Para estos qué opinas desde ambas perspectivas? Es inválido o frontera, no todos pueden estar en el limbo
```

```
def test_division_real_con_decimales():
    assert interpretar ("10 / 4") == 2.5 #Caso frontera por reales y decimanles

Aquí cuál es el veredicto. Así a simple vista, tengo a 2 postulando que es normal o frontera
```

```
Bajo este veredicto, entonces 
def test_division_valida_con_float_decimal():
    ast = OperacionBinaria("/", Numero(13), Numero(2))
    assert evaluar(ast) == 6.5
 

Esta que me dijiste que era frontera
```

```
A ver, ya no hables otros idiomas. Todas las respuestas las quiero en español
```

```
git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 964 bytes | 80.00 KiB/s, done.
From https://github.com/fujonanda/tarea1-mini-interprete
   69dae40..5394b79  tarea1-pruebas-refactorizacion -> origin/tarea1-pruebas-refactorizacion
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint: 
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint: 
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.

Qué fue lo que salió mal?
```

```
=================================================== test session starts ====================================================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.7.0
rootdir: /home/harlow/tarea1-mini-interprete
collected 44 items                                                                                                         

tests/test_evaluator.py .............................                                                                [ 65%]
tests/test_lexer.py .....F..                                                                                         [ 84%]
tests/test_parser.py .....F.                                                                                         [100%]

========================================================= FAILURES =========================================================
___________________________________________ test_respuesta_a_espaciado_irregular ___________________________________________

    def test_respuesta_a_espaciado_irregular():
        # Los espacios múltiples y/o saltos de línea no deben afectar la forma en que se produce la tokenización
        entrada = "  45   \n * \t 2 "
        tokens = tokenizar(entrada)
>       assert tokens == [
            Token(TipoToken.NUMERO, 45, 2),
            Token(TipoToken.POR, "*", 10),
            Token(TipoToken.NUMERO, 2, 14)
        ]
E       AssertionError: assert [Token(NUMERO...UMERO, 2, 13)] == [Token(NUMERO...UMERO, 2, 14)]
E         
E         At index 1 diff: Token(POR, '*', 9) != Token(POR, '*', 10)
E         Use -v to get more diff

tests/test_lexer.py:48: AssertionError
__________________________________________________ test_falta_parentesis ___________________________________________________

    def test_falta_parentesis():
        entrada = "(24 - 27"
>       with pytest.raises(ErrorDeSintaxis, match="se esperaba ')'"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_parser.py:53: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv/lib/python3.11/site-packages/_pytest/raises.py:613: in __init__
    super().__init__(match=match, check=check)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <[AttributeError("'RaisesExc' object has no attribute 'expected_exceptions'") raised in repr()] RaisesExc object at 0x7f5c9c658f90>
match = "se esperaba ')'", check = None

    def __init__(
        self,
        *,
        match: str | Pattern[str] | None,
        check: Callable[[BaseExcT_co], bool] | None,
    ) -> None:
        if isinstance(match, str):
            # juggle error in order to avoid context to fail (necessary?)
            re_error = None
            try:
                self.match: Pattern[str] | None = re.compile(match)
            except re.error as e:
                re_error = e
            if re_error is not None:
>               fail(f"Invalid regex pattern provided to 'match': {re_error}")
E               Failed: Invalid regex pattern provided to 'match': unbalanced parenthesis at position 13

venv/lib/python3.11/site-packages/_pytest/raises.py:381: Failed
================================================= short test summary info ==================================================
FAILED tests/test_lexer.py::test_respuesta_a_espaciado_irregular - AssertionError: assert [Token(NUMERO...UMERO, 2, 13)] == [Token(NUMERO...UMERO, 2, 14)]
FAILED tests/test_parser.py::test_falta_parentesis - Failed: Invalid regex pattern provided to 'match': unbalanced parenthesis at position 13
=============================================== 2 failed, 42 passed in 0.09s ============================

Vaya que no me esperaba esto eh, qué ha salido mal?
```

```
Solo tengo unas dudas. En primer lugar, que se pasen las pruebas no es señal de que esté bien, eso ya lo sabemos. Entonces, qué es lo que me dará la confianza de subir esto sabiendo que algo técnicamente aún está o puede estar mal, y no haber hecho otra prueba me está incapacitando de ver el panorama completo
```

```
No soy ingeniero grosero
```

---

## 4. Cómo se incorporó o se descartó lo obtenido

**Éste es el punto que más pesa.**

| Qué produjo la herramienta | ¿Aceptado, modificado o descartado? | Por qué | Dónde quedó (archivo / commit) |
|---|---|---|---|
| | | | |

> **"Lo descartamos" es una respuesta excelente**, si dicen por qué.
> Una declaración donde todo se aceptó sin cambios es una declaración que
> no muestra criterio.

### 4.1 Si la usaron para el análisis: el contraste

Se les pidió intentarlo primero por su cuenta. Si lo hicieron así:

| | |
|---|---|
| ¿Qué encontró la herramienta que ustedes **no** habían notado? | |
| ¿Qué **no** encontró, que en este curso sí consideramos un problema? | |

> La segunda es la que más nos interesa. Una herramienta suele no señalar la
> duplicación de código, porque el programa funciona igual. Ustedes ya saben
> por qué eso sí importa.
>
> Si no usaron IA para el análisis, escriban *"no aplica"*.

### 4.2 ¿Cómo verificaron que lo que incorporaron era correcto?

> Una prueba que escribieron, una ejecución, un contraste contra las notas de
> clase o contra el enunciado. *"Lo revisamos"* no es una verificación.

---

## 5. Reflexión

### 5.1 ¿Qué limitación concreta observaron **en esta actividad**?

> Concreta. No *"a veces se equivoca"*, sino *"propuso pruebas sólo para
> m = 4 y nunca para órdenes impares, porque no conocía la definición del
> laboratorio"*.

### 5.2 ¿Qué harían distinto la próxima vez?

---

## Firma

> Declaramos que entendemos y podemos explicar todo lo que entregamos,
> independientemente de las herramientas que hayamos utilizado.

| Nombre | Número de cuenta |
|---|---|
| | |

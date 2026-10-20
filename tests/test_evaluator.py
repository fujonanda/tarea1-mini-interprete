"""Pruebas del evaluador: del AST a un numero."""

import pytest
from mini_interprete.cli import interpretar
from mini_interprete.ast import Numero, OperacionBinaria #adicional
from mini_interprete.evaluator import evaluar #adicional
from mini_interprete.errores import ErrorDeEvaluacion, ErrorDeSintaxis

def test_suma():
    assert interpretar("3 + 4") == 7


def test_resta():
    assert interpretar("10 - 3") == 7


def test_multiplicacion():
    assert interpretar("6 * 7") == 42


def test_division():
    assert interpretar("10 / 2") == 5


def test_precedencia_sin_parentesis():
    assert interpretar("3 + 4 * 2") == 11


def test_precedencia_con_parentesis():
    assert interpretar("(3 + 4) * 2") == 14

#Casos normales para operaciones (nótese que las reescribimos respecto al formato de este archivo porque 
# en el README del repositorio se dio otro formato para las pruebas)

def test_parentesis_dentro_de_parentesis_1():
    entrada = "(21 - (4 / 2)) * 3"   # preparar
    resultado = interpretar(entrada)  # ejecutar
    assert resultado == 57.0         # comprobar

def test_parentesis_dentro_de_parentesis_2():
    entrada = "6 + ((7 / 2) * 8)"    # preparar
    resultado = interpretar(entrada)  # ejecutar
    assert resultado == 34.0         # comprobar

# Casos frontera para las operaciones   
def test_suma_de_tres():
    entrada = "10 + 4 + 3"
    resultado = interpretar(entrada)
    assert resultado == 17

def test_resta_de_tres():
    entrada = "10 - 5 - 3"
    resultado = interpretar(entrada)
    assert resultado == 2

def test_multiplicacion_de_tres():
    entrada = "6 * 3 * 2"
    resultado = interpretar(entrada)
    assert resultado == 36

def test_division_de_tres():
    entrada = "50 / 2 / 5"
    resultado = interpretar(entrada)
    assert resultado == 5.0

def test_suma_y_resta():
    entrada = "20 + 10 - 8"
    resultado = interpretar(entrada)
    assert resultado == 22

def test_resta_y_suma():
    entrada = "7 - 4 + 2"
    resultado = interpretar(entrada)
    assert resultado == 5

def test_multiplicacion_y_division():
    entrada = "4 * 20 / 5"
    resultado = interpretar(entrada)
    assert resultado == 16.0

def test_division_y_multiplicacion():
    entrada = "36 / 3 * 2"
    resultado = interpretar(entrada)
    assert resultado == 24.0

def test_division_entre_cero():
    #Este es un caso especial por lo que hemos analizado. Será discutido en ANALISIS.md
    entrada = "10 / 0"
    with pytest.raises(ErrorDeEvaluacion, match="division entre cero"):
        interpretar(entrada)


# Casos inválidos para operaciones

def test_suma_con_negativos():
    entrada = "-3 + -4"
    with pytest.raises(ErrorDeSintaxis):
        interpretar(entrada)

def test_resta_con_negativos():
    entrada = "-10 - -7"
    with pytest.raises(ErrorDeSintaxis):
        interpretar(entrada)

def test_multiplicacion_con_negativos():
    entrada = "-5 * -9"
    with pytest.raises(ErrorDeSintaxis):
        interpretar(entrada)

def test_division_con_negativos():
    entrada = "-16 / -8"
    with pytest.raises(ErrorDeSintaxis):
        interpretar(entrada)


#Casos Normales en AST#

#Estas pruebas en AST se encargan de comprobar a las operaciones básicas en el AST y correcta organización a nivel de nodos
#Explicación de esta eleccioń en DECLARACION_IA.md
def test_suma_basica_en_AST():
    ast = OperacionBinaria("+", Numero(6), Numero(7))
    resultado = evaluar(ast)
    assert resultado == 13    

def test_resta_basica_en_AST():
    ast = OperacionBinaria("-", Numero(9), Numero(3))
    resultado = evaluar(ast)
    assert resultado == 6

def test_producto_basico_en_AST():
    ast = OperacionBinaria("*", Numero(9), Numero(11))
    resultado = evaluar(ast)
    assert resultado == 99

def test_division_valida_con_float_decimal():
    # Otro caso que generó dudas. Será discutido en ANALISIS.md
    ast = OperacionBinaria("/", Numero(13), Numero(2))
    resultado = evaluar(ast)
    assert resultado == 6.5

#Casos frontera en AST#
 
def test_resta_con_resultado_negativo():
    ast = OperacionBinaria("-", Numero(9), Numero(11))
    resultado = evaluar(ast)
    assert resultado == -2


#Casos inválidos en AST#
def test_operador_desconocido_invalido():
    # Evaluator solo conoce +, -, *, / (nuestras operaciones básicas). Cualquier otro símbolo deberá fallar.
    ast = OperacionBinaria("^", Numero(6), Numero(7))
    with pytest.raises(ErrorDeEvaluacion):
        evaluar(ast)

def test_nodo_desconocido():
    # Evaluator debe rechazar objetos que no sean ni 'Numero' ni 'OperacionBinaria' (ej. un string)
    nodo_invalido = "Salu2 bella profesora o bello profesor. Este nodo debe fallar al no ser uno del AST, solo un string"
    with pytest.raises(ErrorDeEvaluacion):
        evaluar(nodo_invalido)

def test_division_por_cero_en_AST():
    ast = OperacionBinaria("/", Numero(93), Numero(0))
    with pytest.raises(ErrorDeEvaluacion, match="division entre cero"):
        evaluar(ast)
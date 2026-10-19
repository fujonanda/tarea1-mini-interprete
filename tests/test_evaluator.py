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

# Casos normales para las peraciones
def test_suma_de_tres():
    assert interpretar("10 + 4 + 3") == 17

def test_multiplicacion_de_tres():
    assert interpretar("6 * 3 * 2") == 36

def test_suma_y_resta():
    assert interpretar("20 + 10 - 8") == 22

def test_suma_y_multiplicacion():
    assert interpretar("20 + 3 * 5") == 35

def test_multiplicacion_y_suma():
    assert interpretar("2 * 4 + 12") == 20

def test_suma_y_division():
    assert interpretar("10 + 9 / 2") == 14.5

def test_division_y_suma():
    assert interpretar("14 / 7 + 5") == 7

def test_resta_y_multiplicacion():
    assert interpretar("3 - 5 * 2") == -7

def test_multiplicacion_y_resta():
    assert interpretar("8 * 4 - 6") == 26

def test_resta_y_division():
    assert interpretar("14 - 5 / 2") == 11.5

def test_division_y_resta():
    assert interpretar("30 / 3 - 4") == 6

def test_multiplicacion_y_division():
    assert interpretar("4 * 20 / 5") == 16

def test_parentesis_dentro_de_parentesis_1():
    assert interpretar("(21 - (4 / 2)) * 3") == 57

def test_parentesis_dentro_de_parentesis_2():
    assert interpretar("6 + ((7 / 2) * 8)") == 34

# Casos frontera para operaciones

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

def test_division_entre_cero():
    with pytest.raises(ErrorDeEvaluacion, match="division entre cero"):
        interpretar("10 / 0")


# Casos inválidos para operaciones

def test_resta_de_tres():
    # Este falla :p
    assert interpretar("10 - 5 - 3") == 2

def test_división_de_tres():
    # falla
    assert interpretar("50 / 2 / 5") == 5

def test_resta_y_suma():
    # falla
    assert interpretar("7 - 4 + 2") == 5

def test_division_y_multiplicacion():
    # falla
    assert interpretar("36 / 3 * 2") == 24
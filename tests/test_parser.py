"""Pruebas del parser: de los tokens al AST."""

import pytest
from mini_interprete.ast import Numero, OperacionBinaria
from mini_interprete.lexer import tokenizar
from mini_interprete.parser import Parser
from mini_interprete.errores import ErrorDeSintaxis


def arbol_de(texto):
    return Parser(tokenizar(texto)).parsear()


def test_construye_el_arbol_de_una_suma():
    assert arbol_de("3 + 4") == OperacionBinaria("+", Numero(3), Numero(4))


def test_la_multiplicacion_se_agrupa_antes_que_la_suma():
    # 3 + 4 * 2  debe agruparse como  3 + (4 * 2)
    assert arbol_de("3 + 4 * 2") == OperacionBinaria(
        "+", Numero(3), OperacionBinaria("*", Numero(4), Numero(2))
    )


def test_los_parentesis_cambian_la_agrupacion():
    # (3 + 4) * 2  debe agruparse al reves
    assert arbol_de("(3 + 4) * 2") == OperacionBinaria(
        "*", OperacionBinaria("+", Numero(3), Numero(4)), Numero(2)
    )


# Casos normales

def test_multiplicacion_abajo_de_la_suma():
    entrada = "7 + 5 * 10"
    resultado = Parser(tokenizar(entrada)).parsear()
    assert resultado == OperacionBinaria("+", Numero(7), OperacionBinaria("*", Numero(5), Numero(10)))


#Casos frontera

def test_orden_izquierda_a_derecha_division():
    # falla
    entrada = "36 / 6 / 3"
    resultado = Parser(tokenizar(entrada)).parsear()
    assert resultado == OperacionBinaria("/", OperacionBinaria("/", Numero(36), Numero(6)), Numero(3))


# Casos inválidos

def test_falta_parentesis():
    entrada = "(24 - 27"
    with pytest.raises(ErrorDeSintaxis, match="se esperaba ')'"):
        Parser(tokenizar(entrada)).parsear()

def test_falta_operador():
    entrada = "2 12"
    with pytest.raises(ErrorDeSintaxis):
        Parser(tokenizar(entrada)).parsear()
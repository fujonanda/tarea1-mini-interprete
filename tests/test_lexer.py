"""Pruebas del lexer: del texto a los tokens."""

import pytest
from mini_interprete.lexer import tokenizar
from mini_interprete.tokens import Token, TipoToken
from mini_interprete.errores import ErrorDeSintaxis



def test_tokeniza_un_numero_solo():
    assert tokenizar("42") == [Token(TipoToken.NUMERO, 42, 0)]


def test_tokeniza_una_suma():
    assert tokenizar("3+4") == [
        Token(TipoToken.NUMERO, 3, 0),
        Token(TipoToken.MAS, "+", 1),
        Token(TipoToken.NUMERO, 4, 2),
    ]


def test_los_espacios_no_producen_tokens():
    assert len(tokenizar("  3   +   4  ")) == 3


def test_tokeniza_parentesis():
    tipos = [token.tipo for token in tokenizar("(3)")]
    assert tipos == [TipoToken.PAR_IZQ, TipoToken.NUMERO, TipoToken.PAR_DER]

#Caso Normal para letzer"

def test_reconocer_operacion_basica():
    # Verifica que reconozca bien números de varios dígitos y los símbolos
    entrada = "13 + 3"
    tokens = tokenizar(entrada)
    assert tokens == [
        Token(TipoToken.NUMERO, 13, 0),
        Token(TipoToken.MAS, "+", 3),
        Token(TipoToken.NUMERO, 3, 5)
    ]

#Caso Frontera del lexer luthor

def test_respuesta_a_espaciado_irregular():
    # Los espacios múltiples y/o saltos de línea no deben afectar la forma en que se produce la tokenización
    entrada = "  45   \n * \t 2 "
    tokens = tokenizar(entrada)
    assert tokens == [
        Token(TipoToken.NUMERO, 45, 2),
        Token(TipoToken.POR, "*", 10),
        Token(TipoToken.NUMERO, 2, 14)
    ]

#Casos Inválidos del rexel

def test_caracter_desconocido_invalido():
    # El lexer actual falla porque ignora el '$' (véase, nuestro símbolo ajeno a los operadores) en lugar de lanzar error
    entrada = "6 $ 9"
    with pytest.raises(ErrorDeSintaxis):
        tokenizar(entrada)

def test_letras_vocabulario_invalido():
    # Las letras no son parte de la gramática y deben ser rechazadas. Aquí no manejamos polinomios.
    entrada = "10a + 5"
    with pytest.raises(ErrorDeSintaxis):
        tokenizar(entrada)


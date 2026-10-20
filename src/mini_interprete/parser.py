"""De los tokens al AST.

La gramatica que reconoce este parser es:

    expresion := termino  (('+' | '-') termino)*
    termino   := factor   (('*' | '/') factor)*
    factor    := NUMERO | '(' expresion ')'

Los tres niveles son lo que hace que  3 + 4 * 2  se agrupe como  3 + (4 * 2)
y no como  (3 + 4) * 2 : la multiplicacion vive un nivel mas abajo, asi que
se arma primero.
"""

from .ast import Numero, OperacionBinaria
from .errores import ErrorDeSintaxis
from .tokens import TipoToken

OPERADORES_SUMA = (TipoToken.MAS, TipoToken.MENOS)
OPERADORES_PRODUCTO = (TipoToken.POR, TipoToken.ENTRE)


class Parser:

    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def parsear(self):
        """Construye el AST de la lista de tokens."""
        if not self.tokens:
            raise ErrorDeSintaxis("Entrada vacia", 0)
            
        resultado = self._expresion()
        
        # Refactorización: Validar que no sobren tokens innecesarios (ej. "2 12")
        actual = self._actual()
        if actual is not None:
            raise ErrorDeSintaxis(f"token inesperado {actual.valor!r}", actual.posicion)
            
        return resultado

    def _actual(self):
        """El token en la posicion actual, o None si ya no quedan."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _avanzar(self):
        """Consume el token actual y lo regresa."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _expresion(self):
        izquierda = self._termino()
        actual = self._actual()
        
        # CAMBIO 1: while preferible sobre if para asociar a la izquierda
        while actual is not None and actual.tipo in OPERADORES_SUMA:
            operador = self._avanzar()
            derecha = self._termino() # Llamamos al nivel inferior, no a _expresion
            # Encadenamos el arbol acumulando hacia la izquierda (arreglamos la asociatividad)
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
            actual = self._actual()
            
        return izquierda

    def _termino(self):
        izquierda = self._factor()
        actual = self._actual()
        
        # CAMBIO 2: while sobre el uso de if para asociar a la izquierda, y por ende corregir la asociatividad mal desarrollada (desde el punto matemático)
        while actual is not None and actual.tipo in OPERADORES_PRODUCTO:
            operador = self._avanzar()
            derecha = self._factor() # Llamamos al nivel inferior
            izquierda = OperacionBinaria(operador.valor, izquierda, derecha)
            actual = self._actual()
            
        return izquierda

    def _factor(self):
        actual = self._actual()
        if actual is None:
            raise ErrorDeSintaxis("se esperaba un numero o '('", self.pos)
            
        token = self._avanzar()

        if token.tipo == TipoToken.NUMERO:
            return Numero(token.valor)

        if token.tipo == TipoToken.PAR_IZQ:
            nodo = self._expresion()
            
            # CAMBIO 3: Proteger al cierre de parentesis contra el fin de la lista (aquí es donde fallaba por no cerrar la expresión)
            cierre = self._actual()
            if cierre is None or cierre.tipo != TipoToken.PAR_DER:
                pos_error = cierre.posicion if cierre else self.pos
                raise ErrorDeSintaxis("se esperaba ')'", pos_error)
            
            self._avanzar() # Consumir el ')'
            return nodo

        raise ErrorDeSintaxis(f"token inesperado {token.valor!r}", token.posicion)
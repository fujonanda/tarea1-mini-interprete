from .ast import Numero, OperacionBinaria
from .errores import ErrorDeEvaluacion


def evaluar(nodo):
    """Evalua un nodo del AST y regresa su valor."""
    match nodo:
        # Caso Base: el valor de Numero sin más
        case Numero(valor=v):
            return v
        
        # Caso Recursivo: extraemos los atributos de la OperacionBinaria
        case OperacionBinaria(operador=op, izquierda=izq, derecha=drc):
            val_izq = evaluar(izq)
            val_drc = evaluar(drc)
            
            # Match anidado para asignar al operador matemático
            match op:
                case "+":
                    return val_izq + val_drc
                case "-":
                    return val_izq - val_drc
                case "*":
                    return val_izq * val_drc
                case "/":
                    if val_drc == 0:
                        raise ErrorDeEvaluacion("division entre cero")
                    return val_izq / val_drc
                
                # Operador no contemplado en la gramática
                case _:
                    raise ErrorDeEvaluacion(f"operador desconocido: {op!r}")

        # Nodo no reconocido (véase un string o un objeto ajeno al AST)
        case _:
            raise ErrorDeEvaluacion(f"nodo desconocido: {nodo!r}")
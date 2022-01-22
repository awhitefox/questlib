from enum import Enum
from typing import Any, Type

from .jsonmapping import *
from .variable import T_VariableValue

__all__ = (
    'Operation',
    'Consequence',
)


class Operation(Enum):
    Set = '='
    Add = '+='
    Subtract = '-='
    Multiply = '*='
    Divide = '/='
    FloorDivide = '//='
    Modulus = '%='

    def eval(self, a: Any, b: Any) -> Any:
        if self == Operation.Set:
            return b
        if self == Operation.Add:
            return a + b
        if self == Operation.Subtract:
            return a - b
        if self == Operation.Multiply:
            return a * b
        if self == Operation.Divide:
            return a / b
        if self == Operation.FloorDivide:
            return a // b
        if self == Operation.Modulus:
            return a % b

    def is_available_for(self, t: Type) -> bool:
        if t is bool:
            return self == Operation.Set
        if t is int or t is float:
            return True
        return False


class Consequence(JsonObject):
    variable_id: str = JsonField()
    type: Operation = JsonField()
    value: T_VariableValue = JsonField()

    def __init__(self, variable_id: str, type_: Operation, value: T_VariableValue):
        self.variable_id = variable_id
        self.type = type_
        self.value = value

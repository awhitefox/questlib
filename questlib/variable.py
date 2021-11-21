from enum import Enum
from typing import Union, Any

from .jsonmapping import *


class VariableDefinition(JsonObject):
    id: str = JsonField()
    name: str = JsonField()
    initial_value: Union[bool, int, float] = JsonField()

    @property
    def type(self):
        return type(self.initial_value)


class OperationType(Enum):
    Set = '='
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'
    Modulus = '%'

    def eval(self, a: Any, b: Any) -> Any:
        if self == OperationType.Set:
            return b
        if self == OperationType.Add:
            return a + b
        if self == OperationType.Subtract:
            return a - b
        if self == OperationType.Multiply:
            return a * b
        if self == OperationType.Divide:
            return a / b
        if self == OperationType.Modulus:
            return a % b


class VariableOperation(JsonObject):
    type: OperationType = JsonField()
    value: Union[bool, int, float]

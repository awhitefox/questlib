from enum import Enum
from typing import Union, Any, Type

from .jsonmapping import *

__all__ = (
    'VariableDefinition',
    'OperationType',
    'VariableOperation'
)


class VariableDefinition(JsonObject):
    id: str = JsonField()
    name: str = JsonField()
    initial_value: Union[bool, float] = JsonField()

    @property
    def type(self):
        return type(self.initial_value)


class OperationType(Enum):
    Set = '='
    Add = '+'
    Subtract = '-'
    Multiply = '*'
    Divide = '/'
    FloorDivide = '//'
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
        if self == OperationType.FloorDivide:
            return a // b
        if self == OperationType.Modulus:
            return a % b

    def is_available_for(self, t: Type) -> bool:
        if t is bool:
            return self == OperationType.Set
        if t is int or t is float:
            return True
        return False


class VariableOperation(JsonObject):
    variable_id: str = JsonField()
    type: OperationType = JsonField()
    value: Union[bool, float] = JsonField()

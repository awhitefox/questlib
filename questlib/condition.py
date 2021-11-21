from enum import Enum
from typing import Any, Union, Type

from .jsonmapping import *

__all__ = (
    'CompareTo',
    'ComparisonType',
    'Condition'
)


class CompareTo(Enum):
    Constant = 'const'
    Variable = 'var'


class ComparisonType(Enum):
    Equal = '=='
    NotEqual = '!='
    Greater = '>'
    GreaterOrEqual = '>='
    Less = '<'
    LessOrEqual = '<='

    def eval(self, a: Any, b: Any) -> bool:
        if self == ComparisonType.Equal:
            return a == b
        if self == ComparisonType.NotEqual:
            return a != b
        if self == ComparisonType.Greater:
            return a > b
        if self == ComparisonType.GreaterOrEqual:
            return a >= b
        if self == ComparisonType.Less:
            return a < b
        if self == ComparisonType.LessOrEqual:
            return a <= b

    def is_available_for(self, t: Type) -> bool:
        if t is bool:
            return self in (ComparisonType.Equal, ComparisonType.NotEqual)
        if t is int or t is float:
            return True
        return False


class Condition(JsonObject):
    compare_to: CompareTo = JsonField()
    comparison: ComparisonType = JsonField()
    left: str = JsonField()
    right: Union[str, float, bool] = JsonField()

from enum import Enum
from typing import Any, Union, Type

from .jsonmapping import *

__all__ = (
    'CompareTo',
    'Comparison',
    'Requirement'
)


class CompareTo(Enum):
    Constant = 'const'
    Variable = 'var'


class Comparison(Enum):
    Equal = '=='
    NotEqual = '!='
    Greater = '>'
    GreaterOrEqual = '>='
    Less = '<'
    LessOrEqual = '<='

    def eval(self, a: Any, b: Any) -> bool:
        if self == Comparison.Equal:
            return a == b
        if self == Comparison.NotEqual:
            return a != b
        if self == Comparison.Greater:
            return a > b
        if self == Comparison.GreaterOrEqual:
            return a >= b
        if self == Comparison.Less:
            return a < b
        if self == Comparison.LessOrEqual:
            return a <= b

    def is_available_for(self, t: Type) -> bool:
        if t is bool:
            return self in (Comparison.Equal, Comparison.NotEqual)
        if t is int or t is float:
            return True
        return False


class Requirement(JsonObject):
    compare_to: CompareTo = JsonField()
    comparison: Comparison = JsonField()
    left: str = JsonField()
    right: Union[str, float, bool] = JsonField()

    def __init__(self, compare_to: CompareTo, comparison: Comparison, left: str, right: Union[str, float, bool]):
        self.compare_to = compare_to
        self.comparison = comparison
        self.left = left
        self.right = right

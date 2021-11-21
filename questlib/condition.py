from enum import Enum
from typing import Any, Union

from .jsonmapping import *


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


class Condition(JsonObject):
    compare_to: CompareTo = JsonField()
    comparison: ComparisonType = JsonField()
    left: str = JsonField()
    right: Union[str, int, float, bool] = JsonField()

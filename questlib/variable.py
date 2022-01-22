from typing import Union

from .jsonmapping import *
from .utils import generate_id

__all__ = (
    'T_VariableValue',
    'Variable'
)
T_VariableValue = Union[bool, float]


class Variable(JsonObject):
    id: str = JsonField()
    name: str = JsonField()
    initial_value: T_VariableValue = JsonField()

    def __init__(self, name: str, initial_value: T_VariableValue):
        self.id = generate_id()
        self.name = name
        self.initial_value = initial_value

    @property
    def type(self):
        return type(self.initial_value)

from typing import List, Optional

from .jsonmapping import *
from . import VariableDefinition, Condition, VariableOperation

__all__ = (
    'Chapter',
    'Branch',
    'Segment',
    'Option',
    'GotoDestination'
)


class Chapter(JsonObject):
    title: str = JsonField()
    variables: List[VariableDefinition] = JsonField()
    branches: List['Branch'] = JsonField()


class Branch(JsonObject):
    id: str = JsonField()
    title: Optional[str] = JsonField(remove_if_none=True)
    segments: List['Segment'] = JsonField()


class Segment(JsonObject):
    id: str = JsonField()
    text: str = JsonField()
    options: Optional[List['Option']] = JsonField(remove_if_none=True)


class Option(JsonObject):
    text: str = JsonField()
    goto: 'GotoDestination' = JsonField()
    conditions: Optional[List[Condition]] = JsonField(remove_if_none=True)
    operations: Optional[List[VariableOperation]] = JsonField(remove_if_none=True)


class GotoDestination(JsonObject):
    branch_id: str = JsonField()
    segment_id: str = JsonField()

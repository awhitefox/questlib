from uuid import uuid4
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

    def __init__(self, title: str):
        self.title = title
        self.variables = []
        self.branches = [Branch(id_='@endings')]


class Branch(JsonObject):
    id: str = JsonField()
    title: Optional[str] = JsonField(remove_if_none=True)
    segments: List['Segment'] = JsonField()

    def __init__(self, title: str = '', *, id_: str = ''):
        self.id = id_ or generate_id()
        self.title = title or self.id
        self.segments = []


class Segment(JsonObject):
    id: str = JsonField()
    text: str = JsonField()
    options: Optional[List['Option']] = JsonField(remove_if_none=True)

    def __init__(self, text: str, *, has_options: bool = True, id_: str = ''):
        self.id = id_ or generate_id()
        self.text = text
        self.options = [] if has_options else None


class Option(JsonObject):
    text: str = JsonField()
    goto: 'GotoDestination' = JsonField()
    conditions: Optional[List[Condition]] = JsonField(remove_if_none=True)
    operations: Optional[List[VariableOperation]] = JsonField(remove_if_none=True)

    def __init__(self, text: str, goto: 'GotoDestination'):
        self.text = text
        self.goto = goto
        self.conditions = None
        self.operations = None


class GotoDestination(JsonObject):
    branch_id: str = JsonField()
    segment_id: str = JsonField()

    def __init__(self, branch_id: str, segment_id: str):
        self.branch_id = branch_id
        self.segment_id = segment_id


def generate_id() -> str:
    return str(uuid4())

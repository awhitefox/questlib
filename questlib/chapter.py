from typing import List, Optional

from .jsonmapping import *
from .utils import generate_id
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
        self.branches = [Branch(id_=Branch.ENDINGS_BRANCH_ID)]


class Branch(JsonObject):
    ENDINGS_BRANCH_ID = '@endings'

    id: str = JsonField()
    title: Optional[str] = JsonField(remove_if_none=True)
    segments: List['Segment'] = JsonField()

    def __init__(self, title: Optional[str] = None, *, id_: str = ''):
        self.id = id_ or generate_id()
        self.title = title
        self.segments = []

    @property
    def is_endings_branch(self) -> bool:
        return self.id == self.ENDINGS_BRANCH_ID


class Segment(JsonObject):
    id: str = JsonField()
    text: str = JsonField()
    options: List['Option'] = JsonList(remove_if_empty=True)

    def __init__(self, text: str, *, has_options: bool = True, id_: str = ''):
        self.id = id_ or generate_id()
        self.text = text
        self.options = [] if has_options else None


class Option(JsonObject):
    text: str = JsonField()
    goto: 'GotoDestination' = JsonField()
    conditions: List[Condition] = JsonList(remove_if_empty=True)
    operations: List[VariableOperation] = JsonList(remove_if_empty=True)

    def __init__(self, text: str, goto: 'GotoDestination'):
        self.text = text
        self.goto = goto
        self.conditions = []
        self.operations = []


class GotoDestination(JsonObject):
    branch_id: str = JsonField()
    segment_id: str = JsonField()

    def __init__(self, branch_id: str, segment_id: str):
        self.branch_id = branch_id
        self.segment_id = segment_id

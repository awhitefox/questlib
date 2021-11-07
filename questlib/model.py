from typing import List, Optional

from jsonmapping import *

__all__ = (
    'Chapter',
    'Branch',
    'Segment',
    'Option',
    'GotoDestination'
)


class Chapter(JsonObject):
    title: str = JsonField()
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


class GotoDestination(JsonObject):
    branch_id: str = JsonField()
    segment_id: str = JsonField()

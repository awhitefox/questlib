import inspect
import json
from enum import Enum
from typing import get_type_hints, Any, Dict, Union, Optional, Tuple

__all__ = (
    'JsonField',
    'JsonList',
    'JsonObject'
)


class JsonField:
    def __init__(self, key: str = '', *, remove_if_none=False):
        self.attr_name = ''
        self.key = key
        self.remove_if_none = remove_if_none

    def __set_name__(self, owner, name):
        self.attr_name = '_' + name
        if self.key == '':
            self.key = name

        # use immutable sequence to avoid issues with inheritance
        if owner._fields is None:
            owner._fields = ()
        owner._fields = (*owner._fields, (name, self))

    def __get__(self, instance, owner):
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        setattr(instance, self.attr_name, value)

    def default_value(self):
        return None


class JsonList(JsonField):
    def __init__(self, key: str = '', *, remove_if_none=False, remove_if_empty=False):
        super(JsonList, self).__init__(key, remove_if_none=remove_if_none)
        self.remove_if_empty = remove_if_empty

    def default_value(self):
        return [] if self.remove_if_empty else None


class JsonObject:
    _fields: Optional[Tuple[Tuple[str, JsonField], ...]] = None

    def _serialize(self) -> Dict[str, Any]:
        if self._fields is None:
            return {}
        result = filter(lambda x: self._check_field(x[1]), self._fields)
        result = map(lambda x: (x[1].key, x[1].__get__(self, None)), result)
        return dict(result)

    def _check_field(self, field: JsonField):
        value = field.__get__(self, None)
        if value is not None:
            if isinstance(field, JsonList) and len(value) == 0 and field.remove_if_empty:
                return False
        elif field.remove_if_none:
            return False
        return True

    def to_json(self, **kwargs) -> str:
        def default(x: Any) -> Any:
            if isinstance(x, JsonObject):
                return x._serialize()
            if isinstance(x, Enum):
                return x.value
            return x
        return json.dumps(self, default=default, **kwargs)

    @classmethod
    def _deserialize(cls, d: Dict[str, Any]) -> 'JsonObject':
        fields = cls._fields
        annotations = get_type_hints(cls)

        c = cls.__new__(cls)
        if fields is not None:
            for attr_name, field in fields:
                annotation = annotations.get(attr_name)
                obj = d.get(field.key)
                if obj is not None:
                    value = _deserialize_object(annotation, obj)
                else:
                    value = field.default_value()
                setattr(c, attr_name, value)
        return c

    @classmethod
    def from_json(cls, s: str, **kwargs) -> 'JsonObject':
        return cls._deserialize(json.loads(s, **kwargs))


def _deserialize_object(annotation: Any, o: Any) -> Any:
    if annotation is not None:
        if inspect.isclass(annotation):
            if issubclass(annotation, JsonObject):
                # noinspection PyProtectedMember
                return annotation._deserialize(o)
            if issubclass(annotation, Enum):
                return annotation(o)
        if hasattr(annotation, '__origin__'):
            origin = annotation.__origin__
            args = annotation.__args__
            if origin is Union:
                return _deserialize_object(args[0], o)
            if origin is list:
                return list(map(lambda x: _deserialize_object(args[0], x), o))
    return o

import inspect
import json
from typing import get_type_hints, Any, Dict, Union

__all__ = (
    'JsonField',
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


class JsonObject:
    _fields = None

    def _serialize(self) -> Dict[str, Any]:
        if self._fields is None:
            return {}
        result = filter(lambda x: not (x[1].__get__(self, None) is None and x[1].remove_if_none), self._fields)
        result = map(lambda x: (x[1].key, x[1].__get__(self, None)), result)
        return dict(result)

    def to_json(self, **kwargs) -> str:
        def default(x: Any) -> Any:
            if isinstance(x, JsonObject):
                return x._serialize()
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
                    value = None
                setattr(c, attr_name, value)
        return c

    @classmethod
    def from_json(cls, s: str, **kwargs) -> 'JsonObject':
        return cls._deserialize(json.loads(s, **kwargs))


def _deserialize_object(annotation: Any, o: Any) -> Any:
    if annotation is not None:
        if inspect.isclass(annotation) and issubclass(annotation, JsonObject):
            # noinspection PyProtectedMember
            return annotation._deserialize(o)
        if hasattr(annotation, '__origin__'):
            origin = annotation.__origin__
            args = annotation.__args__
            if origin is Union:
                return _deserialize_object(args[0], o)
            if origin is list:
                return list(map(lambda x: _deserialize_object(args[0], x), o))
    return o

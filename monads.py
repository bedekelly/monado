from itertools import chain

from typeclasses import Monad, Alternative


class List(Monad, Alternative, implicitly_converts=(list,)):
    def __init__(self, *args, **kwargs):
        self._value = list(*args, **kwargs)

    @property
    def empty(self):
        return List([])

    def __repr__(self):
        return f"List({self._value})"

    def __eq__(self, other):
        return self._value == other

    def apply(self, other):
        return self.bind(lambda item: other.map(lambda f: f(item)))

    @staticmethod
    def with_value(value):
        new_list = List()
        new_list._value = value
        return new_list

    def map(self, function):
        return List([function(x) for x in self._value])

    @classmethod
    def point(cls, value):
        return cls([value])

    def bind(self, f):
        return List(chain.from_iterable([f(x) for x in self._value]))

    def __iter__(self):
        return self._value.__iter__()

    @property
    def items(self):
        return self._value


class Option(Monad, Alternative):
    def __init__(self, value):
        self._value = value

    @property
    def empty(self):
        return Option.nothing()

    def apply(self, functor):
        return self.bind(lambda value: functor.map(lambda f: f(value)))

    def map(self, function):
        if self._value is None:
            return Option.nothing()
        return Option(function(self._value))

    def __repr__(self):
        if self._value is None:
            return "Nothing"
        else:
            return f"Some({self._value})"

    @classmethod
    def point(cls, value):
        return cls(value)

    @classmethod
    def nothing(cls):
        return Option(None)

    def bind(self, f):
        if self._value is None:
            return Option.nothing()
        else:
            return f(self._value)

    def get_or_default(self, default):
        if self._value is None:
            return default
        return self._value

    def is_none(self):
        return self._value is None

    def value(self):
        if self._value is None:
            raise ValueError
        return self._value

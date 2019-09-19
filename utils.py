from types import FunctionType
from typing import TypeVar

from do_notation import do
from typeclasses import Applicative, Monad


def lift_2(f, aa: Applicative, ab: Applicative):
    """
    lifta2 : (a -> b -> c) -> A a -> A b -> A c

    f           : a -> b -> c
    aa          : A a
    ab          : A b
    mapped_func : A (a -> c)
    apply       : A a -> A (a -> c) -> A c
    <returns>   : A c
    """
    mapped_func = ab.map(lambda b: lambda a: f(a, b))
    return aa.apply(mapped_func)


@do
def lift_m2(f, ma, mb):
    a = yield ma
    b = yield mb
    return f(a, b)


@do
def lift_n(function, *monadic_values):
    """
    Lift a function into working on an arbitrary number
    of monadic values.
    """
    values = []
    for monadic_value in monadic_values:
        values.append((yield monadic_value))
    return function(*values)

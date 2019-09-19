from collections import namedtuple

from typeclasses import ImplicitlyConvertible

guard = namedtuple("Guard", "value")


def implicitly_convert(yielded_monad):
    if type(yielded_monad) in ImplicitlyConvertible.conversions:
        new_type = ImplicitlyConvertible.conversions[type(yielded_monad)]
        yielded_monad = new_type(yielded_monad)
    return yielded_monad


def do(f):
    """
    Allow "do notation" for monads using the yield keyword. e.g.:

    @do
    def download_and_process():
        '''Download, decode and process some data.'''
        data    = yield fetch("bede.io")
        decoded = yield decode(data)
        return process(data)


    @do
    def product(l1, l2, l3):
        '''Equivalent to nested for-loops over 3 lists.'''
        x = yield l1
        y = yield l2
        z = yield l3
        return (x, y, z)


    @do
    def sum_optionals(o1, o2, o3):
        '''Only add the numbers if all three are present.'''
        x = yield o1
        y = yield o2
        z = yield o3
        return x + y + z
    """

    def partial_run(f, args, kwargs, monad=None, values_so_far=()):
        # First, create a NEW instance of the coroutine.
        coroutine = f(*args, **kwargs)

        yielded_monad = None

        yielded_values = []

        # Advance the coroutine to the first yield point.
        yielded_value = next(coroutine)
        if not isinstance(yielded_value, guard):
            yielded_monad = implicitly_convert(yielded_value)

        yielded_values.append(yielded_value)

        # For each value so far, send it into the coroutine.
        for v in values_so_far:
            try:
                yielded_value = coroutine.send(v)
                yielded_values.append(yielded_value)
                if not isinstance(yielded_value, guard):
                    yielded_monad = implicitly_convert(yielded_value)

            except StopIteration as ret:
                # This means we've reached the end of the function;
                # lift the return value back into the monad.
                if yielded_monad is None:
                    return monad.empty
                return yielded_monad.point(ret.value)

        def continue_with_value(value):
            """Continue the coroutine execution, pre-filling a given value."""
            return partial_run(f, args, kwargs, monad=(monad or yielded_monad),
                               values_so_far=(*values_so_far, value))

        # If the last yield point was a guard clause, don't "fan out" – just send None in and continue.
        if isinstance(yielded_value, guard):
            return continue_with_value(None) if yielded_value.value else yielded_monad.empty

        # Otherwise bind to the rest of the coroutine.
        return yielded_monad >> continue_with_value

    def wrapped(*args, **kwargs):
        return partial_run(f, args, kwargs)

    return wrapped

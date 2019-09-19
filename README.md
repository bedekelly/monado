# Monads for Python

In the latest of a string of extraordinarily bad decisions, I wrote some
code to use Monads in Python.

In an even worse decision, I decided to make a sort of do-notation work 
as well.

Here's how it looks:

```python
from do_notation import do


@do
def product2(monad_a, monad_b):
    x = yield monad_a
    y = yield monad_b
    return x, y
```

Monads are just written using the `ABC` module and a mini-type-hierarchy
created using inherited abstract methods. It's relatively sane code,
*unlike* how the do-notation is implemented. 

The result of calling `product2(l1, l2)` on two Lists will be a new 
List containing all possible `(x, y)` pairs from the two lists.

Passing in two Option monads gives us a pair `Some((x, y))` if both 
values are filled, and `Nothing` otherwise.

Passing in two Future monads (not yet written) will give a Future of the
combined value `(x, y)`.

This really does work for arbitrary monads. This was hard to get right,
since Python doesn't let you `copy.deepcopy` generators any
more. That meant I had to essentially copy the generator myself by
recursively calling the function with an accumulated list of values we'd
already passed to it in that particular `bind`.

The one teeny tiny gotcha is that side effects only really work how
you'd expect them to work right at the *end* of the function. So
interleaving `print` calls with the yield statements will give
weird results. That's a result of how I'm "copying" the generators.
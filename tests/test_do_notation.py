import itertools as it

from do_notation import do, guard
from monads import List, Option


def test_list_product():
    @do
    def product2(monad_a, monad_b):
        x = yield monad_a
        y = yield monad_b
        return x, y

    l1 = List([1, 2])
    l2 = List("ab")
    assert product2(l1, l2).items == [(1, "a"), (1, "b"), (2, "a"), (2, "b")]


def test_iterated_list():
    @do
    def product(*lists):
        values = []
        for l in lists:
            values.append((yield l))
        return tuple(values)

    l1 = List([1, 2])
    l2 = List("ab")
    l3 = List("xyz")
    l4 = List([90, 100])

    expected = list(it.product(l1, l2, l3, l4))
    assert expected == product(l1, l2, l3, l4).items


def test_options():
    @do
    def add(monad_a, monad_b):
        x = yield monad_a
        y = yield monad_b
        return x + y

    oN = Option(None)
    o1 = Option(1)
    o2 = Option(2)
    assert add(o1, o2).value() == 3
    assert add(oN, o1).is_none()
    assert add(o2, oN).is_none()


def test_guard():
    @do
    def only_evens():
        a = yield List(range(10))
        _ = yield guard(a % 2 == 0)
        return a

    assert only_evens().items == [0, 2, 4, 6, 8]


def test_coins():

    toss = {"Fair": ["Heads", "Tails"], "Biased": ["Heads", "Heads"]}

    @do
    def coins():
        coin   = yield ["Fair", "Biased"]
        result = yield toss[coin]
        _      = yield guard(result == "Heads")
        return coin

    # Probability of a biased coin, given you observed Heads, is 2/3.
    assert coins() == ["Fair", "Biased", "Biased"]


def test_change():

    @do
    def money(amount_owed, possible_coins):
        change = []
        while amount_owed > 0 and possible_coins:
            give_max_coin = yield [True, False]
            if give_max_coin:
                max_coin = possible_coins[-1]
                change.append(max_coin)
                amount_owed -= max_coin
            else:
                possible_coins = possible_coins[:-1]
        yield guard(amount_owed == 0)
        return change

    assert len(money(23, [1, 2, 20]).items) == 14

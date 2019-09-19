from monads import List, Option
from utils import lift_2, lift_n


def test_lift_2_lists():
    # Test liftA2 function gives cartesian product on lists.
    l1 = List([1, 2])
    l2 = List(["a", "b"])

    assert lift_2(lambda a, b: (a, b), l1, l2).items == [
        (1, "a"),
        (1, "b"),
        (2, "a"),
        (2, "b"),
    ]


def test_list_2_optionals():
    # Test lifta2 function for optionals.
    optA = Option.point(2)
    optB = Option.point(None)
    optC = Option.point(3)

    def crash(a, b):
        assert False, "This function shouldn't be run."

    # This shouldn't error:
    lift_2(crash, optA, optB)

    # This should give a result of 6:
    mul = lambda a, b: a * b
    assert lift_2(mul, optA, optC).value() == 6


def test_lift_n_optionals():
    sum_varying = lambda *args: sum(args)
    options = map(Option, range(1, 10))
    assert lift_n(sum_varying, *options).value() == sum(range(1, 10))

    none_option = Option(None)
    assert lift_n(sum_varying, none_option, *options).is_none()
    assert lift_n(sum_varying, *options, none_option).is_none()


def test_lift_n_lists():
    sum_varying = lambda *args: sum(args)

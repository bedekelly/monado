from monads import Option, List
from utils import lift_2


def test_option_none():
    opt = (
        Option.point(10)
        >> (lambda x: Option.point(x + 5))
        >> (lambda y: Option.point(y + 10))
        >> (lambda z: Option.point(None))
        >> (lambda x: Option.point(x + 1))
    )
    assert opt.is_none()


def test_option_not_none():
    # Test is_none method (false)
    opt2 = Option.point(0.5) >> (lambda x: Option.point(x + 10))
    assert not opt2.is_none()


def test_option_get_or_default():
    # Test get_or_default method.
    opt3 = (
        Option.point(3)
        >> (lambda x: Option.point(x + 5))
        >> (lambda y: Option.point(y + 2))
    )
    assert opt3.get_or_default(0) == 10


def test_option_value():
    # Test .value() method.
    opt4 = Option.point(10).map(lambda x: x + 10).value()
    assert opt4 == 20


def test_list_bind():
    opt5 = List([1, 2, 3]) >> (lambda x: List([x + 10]))
    assert opt5.items == [11, 12, 13]
    assert opt5.bind(lambda x: List([x * 10])).items == [110, 120, 130]


def test_list_map():
    opt6 = List([1, 2, 3]).map(lambda x: x + 1)
    assert opt6.items == [2, 3, 4]


def test_optional_map():
    opt = Option(None)

    def broken():
        assert False

    opt.map(lambda a: broken)

    opt = Option(3)
    assert opt.map(lambda x: x + 1).value() == 4


def test_optional_apply():
    optN = Option(None)
    optF = Option(lambda a: a + 1)
    assert optN.apply(optF).is_none()
    opt3 = Option(3)
    assert opt3.apply(optF).value() == 4


def test_apply_method():
    # Test List's apply method
    opt7 = List([1, 2, 3]).apply(List.point(lambda x: x + 1))
    assert opt7.items == [2, 3, 4]


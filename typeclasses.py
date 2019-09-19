from abc import abstractmethod, ABC


class ImplicitlyConvertible:
    conversions = {}

    def __init_subclass__(cls, implicitly_converts=None, **kwargs):
        if implicitly_converts is not None:
            for type_ in implicitly_converts:
                ImplicitlyConvertible.conversions[type_] = cls
        return super().__init_subclass__(**kwargs)


class Functor(ImplicitlyConvertible, ABC):
    @abstractmethod
    def map(self, function):
        """
        map: F a -> (a -> b) -> F b
        """
        raise NotImplementedError


class Applicative(Functor):
    @classmethod
    @abstractmethod
    def point(cls, value):
        """
        point : a -> A a
        """
        raise NotImplementedError

    @abstractmethod
    def apply(self, other):
        """
        apply : A a -> A (a -> b) -> A b
        """
        raise NotImplementedError


class Alternative(Applicative):
    @abstractmethod
    def empty(self):
        raise NotImplementedError


class Monad(Applicative):
    @abstractmethod
    def bind(self, f):
        """
        bind : M a -> (a -> M b) -> M b
        """
        raise NotImplementedError

    def __rshift__(self, f):
        return self.bind(f)

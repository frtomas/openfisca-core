import functools
import warnings
import typing
from typing import Any, Callable, Type, TypeVar

from openfisca_core.types import Descriptable

ProtType = TypeVar("ProtType")
DescType = TypeVar("DescType")
FuncType = TypeVar("FuncType", bound = Callable[..., Any])


class composed:

    def __init__(self, protocol: Type[ProtType]) -> None:
        self.protocol = protocol

    def __call__(self, composed: Type[DescType]) -> Type[DescType]:
        composed.__annotations__ = self.protocol.__annotations__
        return composed


class descripted:

    def __init__(self, descriptor: Type[Descriptable]) -> None:
        self.descriptor = descriptor

    def __call__(self, descripted: Type[DescType]) -> Type[DescType]:
        setattr(descripted, self.descriptor.private_name, None)
        setattr(descripted, self.descriptor.public_name, self.descriptor())
        return descripted


class deprecated:

    def __init__(self, since: str, expires: str) -> None:
        self.since = since
        self.expires = expires

    def __call__(self, function: FuncType) -> FuncType:
        self.function = function

        def wrapper(*args: Any, **kwds: Any) -> Any:
            message = [
                f"{self.function.__qualname__} has been deprecated since",
                f"version {self.since}, and will be removed in",
                f"{self.expires}.",
                ]
            warnings.warn(" ".join(message), DeprecationWarning)
            return self.function(*args, **kwds)

        functools.update_wrapper(wrapper, function)
        return typing.cast(FuncType, wrapper)

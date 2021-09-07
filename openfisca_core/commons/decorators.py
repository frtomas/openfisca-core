import functools
import warnings
import typing
from typing import Any, Callable, TypeVar

FuncType = TypeVar("FuncType", bound = Callable[..., Any])


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

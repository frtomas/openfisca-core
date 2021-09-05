import functools
import warnings
import typing
from typing import Any

from openfisca_core.types import ArgsType, KwdsType, DecoType, FuncType


def deprecated(since: str, expires: str) -> DecoType:
    return functools.partial(decorator, since = since, expires = expires)


def decorator(function: FuncType, since: str, expires: str) -> FuncType:

    @functools.wraps(function)
    def wrapper(*args: Any, **kwds: Any) -> Any:
        message = [
            f"{function.__qualname__} has been deprecated since version",
            f"{since}, and will be removed in {expires}.",
            ]
        warnings.warn(" ".join(message), DeprecationWarning)
        return function(*args, **kwds)

    return typing.cast(FuncType, wrapper)

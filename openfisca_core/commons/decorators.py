import functools
import warnings
from typing import Any

from openfisca_core.types import ArgsType, KwdsType, DecoType


def deprecated(since: str, expires: str) -> DecoType:
    return functools.partial(decorator, since = since, expires = expires)


def decorator(function: DecoType, since: str, expires: str) -> DecoType:

    @functools.wraps(function)
    def wrapper(*args: ArgsType, **kwds: KwdsType) -> Any:
        message = [
            f"{function.__qualname__} has been deprecated since version",
            f"{since}, and will be removed in {expires}.",
            ]
        warnings.warn(" ".join(message), DeprecationWarning)
        return function(*args, **kwds)

    return wrapper

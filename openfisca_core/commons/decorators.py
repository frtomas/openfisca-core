import functools
import warnings
from typing import Any

from openfisca_core.types import Args, Kwds, Decorator


def deprecated(since: str, expires: str) -> Decorator:
    return functools.partial(decorator, since = since, expires = expires)


def decorator(function: Decorator, since: str, expires: str) -> Decorator:

    @functools.wraps(function)
    def wrapper(*args: Args, **kwds: Kwds) -> Any:
        message = [
            f"{function.__qualname__} has been deprecated since version",
            f"{since}, and will be removed in {expires}.",
            ]
        warnings.warn(" ".join(message), DeprecationWarning)
        return function(*args, **kwds)

    return wrapper

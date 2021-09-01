import functools
import warnings
from typing import Callable


def deprecated(since: str, expires: str) -> Callable:
    return functools.partial(decorator, since = since, expires = expires)


def decorator(function: Callable, since: str, expires: set) -> Callable:

    @functools.wraps(function)
    def wrapper(*args, **kwds):
        message = [
            f"{function.__qualname__} has been deprecated since version",
            f"{since}, and will be removed in {expires}.",
            ]
        warnings.warn(" ".join(message), DeprecationWarning)
        return function(*args, **kwds)

    return wrapper

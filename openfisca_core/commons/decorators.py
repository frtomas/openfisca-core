import functools
import warnings

from openfisca_core.types import Decorator


def deprecated(since: str, expires: str) -> Decorator:
    return functools.partial(decorator, since = since, expires = expires)


def decorator(function: Decorator, since: str, expires: set) -> Decorator:

    @functools.wraps(function)
    def wrapper(*args, **kwds):
        message = [
            f"{function.__qualname__} has been deprecated since version",
            f"{since}, and will be removed in {expires}.",
            ]
        warnings.warn(" ".join(message), DeprecationWarning)
        return function(*args, **kwds)

    return wrapper

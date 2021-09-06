from typing import Iterable, Optional
from typing_extensions import TypedDict


class RoleLike(TypedDict, total = False):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    subroles: Optional[Iterable[str]]

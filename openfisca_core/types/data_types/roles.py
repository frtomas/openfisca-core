from typing import Sequence, Optional
from typing_extensions import TypedDict

SubrolesLike = Sequence[str]


class RoleLike(TypedDict, total = False):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    subroles: Optional[SubrolesLike]


RolesLike = Sequence[RoleLike]

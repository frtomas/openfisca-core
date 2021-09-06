from typing import List, Optional
from typing_extensions import TypedDict

SubrolesLike = List[str]


class RoleLike(TypedDict, total = False):
    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: Optional[str]
    max: Optional[int]
    subroles: Optional[SubrolesLike]


RolesLike = List[RoleLike]

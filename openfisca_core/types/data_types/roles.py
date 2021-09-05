from typing import Dict, List, Union


SubrolesLike = List[str]

RoleLike = Dict[str, Union[str, SubrolesLike]]

RolesLike = List[RoleLike]

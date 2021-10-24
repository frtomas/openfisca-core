from __future__ import annotations

from typing import Any, Optional, Sequence

from dataclasses import dataclass

from openfisca_core.types import HasRoles, SupportsRole

from openfisca_core import commons
from openfisca_core.entities import Entity, Role

from .role import RoleLike


@dataclass
class GroupEntity(Entity):
    """Represents a :class:`.GroupEntity` on which calculations can be run.

    A :class:`.GroupEntity` is basically a group of people, and thus it is
    composed of several :obj:`Entity` with different :obj:`Role` within the
    group. For example a tax household, a family, a trust, etc.

    Attributes:
        key: Key to identify the :class:`.GroupEntity`.
        plural: The ``key``, pluralised.
        label: A summary description.
        doc: A full description, dedented.
        is_person: Represents an individual? Defaults to False.
        roles: List of the roles of the group entity.
        flattened_roles: ``roles`` flattened out.

    Args:
        key: Key to identify the :class:`.GroupEntity`.
        plural: ``key``, pluralised.
        label: A summary description.
        doc: A full description.
        roles: The list of :class:`.Role` of the :class:`.GroupEntity`.

    Examples:
        >>> roles = [{
        ...     "key": "parent",
        ...     "subroles": ["first_parent", "second_parent"],
        ...     }]

        >>> group_entity = GroupEntity(
        ...     "household",
        ...     "households",
        ...     "A household",
        ...     "All the people who live together in the same place.",
        ...     roles,
        ...    )

        >>> repr(GroupEntity)
        "<class 'openfisca_core.entities.group_entity.GroupEntity'>"

        >>> repr(group_entity)
        'GroupEntity(household)'

        >>> str(group_entity)
        'households'

    .. versionchanged:: 35.7.0
        Added documentation, doctests, and typing.

    """

    __slots__ = tuple((
        "key",
        "plural",
        "label",
        "doc",
        "is_person",
        "roles",
        "flattened_roles",
        "roles_description",
        "_tax_benefit_system",
        ))

    is_person: bool
    roles: Sequence[SupportsRole]
    flattened_roles: Sequence[SupportsRole]
    roles_description: Sequence[RoleLike]

    def __init__(
            self,
            key: str,
            plural: str,
            label: str,
            doc: str,
            roles: Sequence[RoleLike],
            ):
        super().__init__(key, plural, label, doc)
        self.is_person = False
        self.roles = tuple(build_role(self, desc) for desc in roles)
        self.flattened_roles = flatten_roles(self.roles)
        self.roles_description = roles

    def __getattr__(self, attr: str) -> Any:
        if attr.isupper():
            return self._role(attr)

        return self.__getattribute__(attr)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.key})"

    def __str__(self) -> str:
        return self.plural

    def _role(self, upper: str) -> Optional[SupportsRole]:
        """Searches and returns the requested :obj:`.Role`.

        Args:
            upper: The role key, uppercased.

        Returns:
            Role: The requested :obj:`.Role`.
            None: Otherwise.

        Examples:
            >>> entity = GroupEntity("", "", "", "", ())
            >>> role = Role({"key": "key"}, entity)
            >>> entity.roles += role,

            >>> entity._role(role.key.upper())
            Role(key)

            >>> entity._role(role.key)

        .. versionadded:: 35.7.0

        """

        where = (
            role
            for role in (*self.roles, *self.flattened_roles)
            if role.key.upper() == upper
            )

        return commons.first(where)


def build_role(entity: HasRoles, description: RoleLike) -> SupportsRole:
    """Build roles & sub-roles."""

    role = Role(description, entity)
    subroles = description.get("subroles", ())

    if subroles:
        role.subroles = ()

        for key in subroles:
            subrole = Role({"key": key, "max": 1}, entity)
            role.subroles = (*role.subroles, subrole)

        role.max = len(role.subroles)

    return role


def flatten_roles(roles: Sequence[SupportsRole]) -> Sequence[SupportsRole]:
    tree = [role.subroles or [role] for role in roles]
    return tuple(commons.flatten(tree))

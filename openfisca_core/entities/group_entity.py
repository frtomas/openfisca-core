from __future__ import annotations

from dataclasses import dataclass

from openfisca_core.entities import Entity, Role


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

    def __init__(self, key, plural, label, doc, roles):
        super().__init__(key, plural, label, doc)
        self.roles_description = roles
        self.roles = []
        for role_description in roles:
            role = Role(role_description, self)
            setattr(self, role.key.upper(), role)
            self.roles.append(role)
            if role_description.get('subroles'):
                role.subroles = []
                for subrole_key in role_description['subroles']:
                    subrole = Role({'key': subrole_key, 'max': 1}, self)
                    setattr(self, subrole.key.upper(), subrole)
                    role.subroles.append(subrole)
                role.max = len(role.subroles)
        self.flattened_roles = sum([role2.subroles or [role2] for role2 in self.roles], [])
        self.is_person = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.key})"

    def __str__(self) -> str:
        return self.plural

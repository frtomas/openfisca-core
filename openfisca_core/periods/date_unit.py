from __future__ import annotations

import enum
from typing import Any, Tuple, TypeVar

from openfisca_core.indexed_enums import Enum

T = TypeVar("T", bound = "DateUnit")


class DateUnitMeta(enum.EnumMeta):

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, str):
            return super().__contains__(self[item.upper()])

        return super().__contains__(item)

    def __getitem__(self, key: object) -> T:
        if not isinstance(key, (int, slice, str, DateUnit)):
            return NotImplemented

        if isinstance(key, (int, slice)):
            return self[self.__dict__["_member_names_"][key]]

        if isinstance(key, str):
            return super().__getitem__(key.upper())

        return super().__getitem__(key.value.upper())

    @property
    def ethereal(self) -> Tuple[DateUnit, ...]:
        """Creates a :obj:`tuple` of ``key`` with ethereal items.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> DateUnit.ethereal
            (<DateUnit.DAY(day)>, <DateUnit.MONTH(month)>, <DateUnit.YEAR(year)>)

            >>> DateUnit.DAY in DateUnit.ethereal
            True

            >>> "DAY" in DateUnit.ethereal
            True

            >>> "day" in DateUnit.ethereal
            True

            >>> "eternity" in DateUnit.ethereal
            False

        """

        return DateUnit.DAY, DateUnit.MONTH, DateUnit.YEAR

    @property
    def eternal(self) -> Tuple[DateUnit, ...]:
        """Creates a :obj:`tuple` of ``key`` with eternal items.

        Returns:
            tuple(str): A :obj:`tuple` containing the ``keys``.

        Examples:
            >>> DateUnit.eternal
            (<DateUnit.ETERNITY(eternity)>,)

            >>> DateUnit.ETERNITY in DateUnit.eternal
            True

            >>> "ETERNITY" in DateUnit.eternal
            True

            >>> "eternity" in DateUnit.eternal
            True

            >>> "day" in DateUnit.eternal
            False

        """

        return (DateUnit.ETERNITY,)


class DateUnit(Enum, metaclass = DateUnitMeta):
    """The date units of a rule system.

    Attributes:
        index (:obj:`int`): The ``index`` of each item.
        name (:obj:`str`): The ``name`` of each item.
        value (tuple(str, int)): The ``value`` of each item.

    Examples:
        >>> repr(DateUnit)
        "<enum 'DateUnit'>"

        >>> repr(DateUnit.DAY)
        '<DateUnit.DAY(day)>'

        >>> str(DateUnit.DAY)
        'day'

        >>> dict([(DateUnit.DAY, DateUnit.DAY.value)])
        {<DateUnit.DAY(day)>: 'day'}

        >>> tuple(DateUnit)
        (<DateUnit.WEEK_DAY(week_day)>, <DateUnit.WEEK(week)>, <DateUnit.DA...)

        >>> len(DateUnit)
        6

        >>> DateUnit["DAY"]
        <DateUnit.DAY(day)>

        >>> DateUnit["day"]
        <DateUnit.DAY(day)>

        >>> DateUnit[2]
        <DateUnit.DAY(day)>

        >>> DateUnit[-4]
        <DateUnit.DAY(day)>

        >>> DateUnit[DateUnit.DAY]
        <DateUnit.DAY(day)>

        >>> DateUnit("day")
        <DateUnit.DAY(day)>

        >>> DateUnit.DAY in DateUnit
        True

        >>> "DAY" in DateUnit
        True

        >>> "day" in DateUnit
        True

        >>> DateUnit.DAY == DateUnit.DAY
        True

        >>> "DAY" == DateUnit.DAY
        True

        >>> "day" == DateUnit.DAY
        True

        >>> DateUnit.DAY < DateUnit.DAY
        False

        >>> DateUnit.DAY > DateUnit.DAY
        False

        >>> DateUnit.DAY <= DateUnit.DAY
        True

        >>> DateUnit.DAY >= DateUnit.DAY
        True

        >>> "DAY" < DateUnit.DAY
        False

        >>> "DAY" > DateUnit.DAY
        False

        >>> "DAY" <= DateUnit.DAY
        True

        >>> "DAY" >= DateUnit.DAY
        True

        >>> "day" < DateUnit.DAY
        False

        >>> "day" > DateUnit.DAY
        False

        >>> "day" <= DateUnit.DAY
        True

        >>> "day" >= DateUnit.DAY
        True

        >>> DateUnit.DAY.index
        2

        >>> DateUnit.DAY.name
        'DAY'

        >>> DateUnit.DAY.value
        'day'

    .. versionadded:: 35.9.0

    """

    # Attributes

    index: int
    name: str
    value: str

    # Members

    WEEK_DAY = "week_day"
    WEEK = "week"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    ETERNITY = "eternity"

    __hash__ = object.__hash__

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other.lower()

        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.index < DateUnit[other.upper()].index

        return self.index < other

    def __le__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.index <= DateUnit[other.upper()].index

        return self.index <= other

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.index > DateUnit[other.upper()].index

        return self.index > other

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.index >= DateUnit[other.upper()].index

        return self.index >= other

    def upper(self) -> str:
        """Uppercases the :class:`.Unit`.

        Returns:
            :obj:`str`: The uppercased :class:`.Unit`.

        Examples:
            >>> DateUnit.DAY.upper()
            'DAY'

        """

        return self.value.upper()

    def lower(self) -> str:
        """Lowecases the :class:`.Unit`.

        Returns:
            :obj:`str`: The lowercased :class:`.Unit`.

        Examples:
            >>> DateUnit.DAY.lower()
            'day'

        """

        return self.value.lower()
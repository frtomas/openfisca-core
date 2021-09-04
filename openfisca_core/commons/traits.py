import abc
import dataclasses
import textwrap
from typing import Optional


class Documentable(abc.ABC):

    @property
    def doc(self) -> str:
        return self.__doc

    @doc.setter
    def doc(self, value: str) -> None:
        self.__doc = textwrap.dedent(value)


@dataclasses.dataclass(repr = False)
class Personifiable(Documentable, abc.ABC):

    key: str
    plural: Optional[str]
    label: Optional[str]
    doc: str


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(Personifiable, abc.ABC):

    ...


class Aggregatable(abc.ABC):

    ...


class Representable(abc.ABC):

    @abc.abstractmethod
    def get_variable(self, variable_name, check_existence):
        ...

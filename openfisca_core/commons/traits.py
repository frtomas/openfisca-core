import abc
import dataclasses
import textwrap


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
    plural: str
    label: str
    doc: str


@dataclasses.dataclass(init = False, repr = False)
class Rolifiable(Personifiable, abc.ABC):
    ...

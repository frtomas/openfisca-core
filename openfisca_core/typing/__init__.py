"""Data types and protocols used by OpenFisca Core.

The type definitions included in this sub-package are intented for
contributors, to help them better understand and document contracts
and expected behaviours.

Official Public API:
    * :data:`.ArrayLike`
    * :attr:`.ArrayType`
    * :class:`.EntityProtocol`
    * :class:`.FormulaProtocol`
    * :class:`.GroupEntityProtocol`
    * :class:`.RoleProtocol`
    * :class:`.TaxBenefitSystemProtocol`
    * :class:`.GroupEntityProtocol`
    * :class:`.RoleProtocol`
    * :class:`.TaxBenefitSystemProtocol`
    * :class:`.VariableProtocol`
    * :class:`.RoleSchema`

Note:
    How imports are being used today::

        from openfisca_core.typing import *  # Bad
        from openfisca_core.typing._types import ArrayLike  # Bad


    The previous examples provoke cyclic dependency problems, that prevents us
    from modularizing the different components of the library, so as to make
    them easier to test and to maintain.

    How could them be used after the next major release::

        from openfisca_core.typing import ArrayLike

        ArrayLike # Good: import types as publicly exposed

    .. seealso:: `PEP8#Imports`_ and `OpenFisca's Styleguide`_.

    .. _PEP8#Imports:
        https://www.python.org/dev/peps/pep-0008/#imports

    .. _OpenFisca's Styleguide:
        https://github.com/openfisca/openfisca-core/blob/master/STYLEGUIDE.md

"""

# Official Public API

from ._types import (  # noqa: F401
    ArrayLike,
    ArrayType,
    )

__all__ = ["ArrayLike", "ArrayType"]

from ._protocols import (  # noqa: F401
    EntityProtocol,
    FormulaProtocol,
    GroupEntityProtocol,
    RoleProtocol,
    TaxBenefitSystemProtocol,
    VariableProtocol,
    )

__all__ = ["EntityProtocol", "GroupEntityProtocol", "RoleProtocol", *__all__]
__all__ = ["FormulaProtocol", "TaxBenefitSystemProtocol", *__all__]
__all__ = ["VariableProtocol", *__all__]

from ._schemas import RoleSchema  # noqa: F401

__all__ = ["RoleSchema", *__all__]
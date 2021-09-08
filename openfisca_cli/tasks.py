import os
import sys

import invoke

from openfisca_core.scripts import openfisca_command
from openfisca_core.scripts.run_test import main as _test
from openfisca_web_api.scripts.serve import main as _serve

@invoke.task(
    help = {
        "path": "Paths (files or directories) of tests to execute.",
        },
    )
def test(_, path, workers = None):
    """Run OpenFisca tests.

    Examples:
        $ openfica test "$(git ls-files 'tests/**/*.py')"

    """

    # Pseudo-implementation of `openfisca test`
    sys.argv = sys.argv[0:2] + path.split()
    _test(openfisca_command.get_parser())


@invoke.task(
    optional = ["extensions"],
    help = {
        "country-package": "Country package to use.",
        "extensions": "Extensions to load.",
        },
    )
def serve(_, country_package, extensions = None):
    """Run the OpenFisca Web API.

    Examples:
        $ openfica serve --country-package openfisca_country_template

    """

    # Pseudo-implementation of `openfisca serve`
    _serve(openfisca_command.get_parser())

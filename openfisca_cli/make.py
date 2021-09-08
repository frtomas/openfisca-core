import sys

import invoke

from . import tasks


@invoke.task
def clean(context):
    """Delete builds and compiled python files."""

    info(clean)

    context.run("rm -rf build dist")
    context.run("find . -name '*.pyc' | xargs rm -f")


@invoke.task
def check_syntax_errors(context):
    """Compile python files to check for syntax errors."""

    info(check_syntax_errors)

    context.run("python -m compileall -q .")


@invoke.task
def check_style(context):
    """Run linters to check for syntax and style errors."""

    info(check_style)

    context.run("flake8 openfisca_core openfisca_web_api")


@invoke.task
def format_style(context):
    """Run code formatters to correct style errors."""

    info(format_style)

    context.run("autopep8 openfisca_core openfisca_web_api")


@invoke.task
def check_types(context):
    """Run static type checkers for type errors."""

    info(check_types)

    context.run("mypy openfisca_core openfisca_web_api")


@invoke.task
def test(context, workers = None):
    """Run openfisca-core tests."""

    info(test)

    path = context.run("git ls-files 'tests/*.py'", hide = "out").stdout
    sys.argv = sys.argv[0:1] + ["test"] + path.split()
    tasks.test(context, path)


@invoke.task
def api(context):
    """Serve the openfisca Web API."""

    sys.argv[1] = "serve"

    tasks.serve(
        context,
        "openfisca_country_template",
        "openfisca_extension_template",
        )

def info(func):
    doc = func.__doc__.split('\n')[0]
    print(f"[⚙] {doc}..")


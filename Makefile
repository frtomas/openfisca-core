help = sed -n "/^$1/ { x ; p ; } ; s/\#\#/[⚙]/ ; s/\./.../ ; x" ${MAKEFILE_LIST}
repo = https://github.com/openfisca/openfisca-doc
branch = $(shell git branch --show-current)

## Same as `make test`.
all: test

## Install project dependencies.
install:
	@$(call help,$@:)
	@pip install --upgrade pip twine wheel
	@pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

## Install openfisca-core for deployment and publishing.
build: setup.py
	@## This allows us to be sure tests are run against the packaged version
	@## of openfisca-core, the same we put in the hands of users and reusers.
	@$(call help,$@:)
	@python $? bdist_wheel
	@find dist -name "*.whl" -exec pip install --force-reinstall {}[dev] \;

## Uninstall project dependencies.
uninstall:
	@$(call help,$@:)
	@pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

## Delete builds and compiled python files.
clean: \
	$(shell ls -d * | grep "build\|dist") \
	$(shell find . -name "*.pyc")
	@$(call help,$@:)
	@rm -rf $?

## Compile python files to check for syntax errors.
check-syntax-errors: .
	@$(call help,$@:)
	@python -m compileall -q $?

## Run static type checkers for type errors.
check-types: \
	check-types-strict-types \
	check-types-strict-entities \
	check-types-strict-commons \
	check-types-all \
	;

## Run static type checkers for type errors.
check-types-all:
	@$(call help,$@:)
	@mypy --package openfisca_core --package openfisca_web_api

## Run static type checkers for type errors.
check-types-strict-%:
	@$(call help,$@:)
	@mypy --cache-dir .mypy_cache-openfisca_core.$* --implicit-reexport --strict --package openfisca_core.$*

## Run linters to check for syntax and style errors.
check-style: \
	check-style-doc-types \
	check-style-doc-entities \
	check-style-doc-commons \
	check-style-all \
	;

## Run linters to check for syntax and style errors.
check-style-all:
	@$(call help,$@:)
	@flake8 --extend-ignore=D `git ls-files | grep "\.py$$"`

## Run linters to check for syntax and style errors.
check-style-doc-%:
	@$(call help,$@:)
	@flake8 --select=D101,D102,D103,DAR openfisca_core/$*

## Run code formatters to correct style errors.
format-style: $(shell git ls-files "*.py")
	@$(call help,$@:)
	@autopep8 $?

## Run openfisca-core tests.
test: clean check-syntax-errors
	@${MAKE} test-python ;
	@${MAKE} check-types ;
	@${MAKE} check-style ;

test-python: \
	test-python-1 \
	test-python-2 \
	test-python-3 \
	test-python-4 \
	;

test-python-%: \
	$(shell git ls-files "openfisca_core/entities/**/*.py") \
	$(shell git ls-files "openfisca_core/commons/**/*.py") \
	$(shell git ls-files "tests/**/*.py")
	@$(eval total := $(shell echo $? | wc -w))
	@$(eval split := $(shell echo $$(( (${total} + 3 ) / 4 ))))
	@$(eval chunk := $(shell echo $? | cut -d" " -f $$(( ${split} * $* + 1 ))-$$(( ${split} * ( $* + 1 ) ))))
	@PYTEST_ADDOPTS="${PYTEST_ADDOPTS}" pytest ${chunk}

## Check that the current changes do not break the doc.
test-doc:
	@##	Usage:
	@##
	@##		make test-doc [branch=BRANCH]
	@##
	@##	Examples:
	@##
	@##		# Will check the current branch in openfisca-doc.
	@##		make test-doc
	@##
	@##		# Will check "test-doc" in openfisca-doc.
	@##		make test-doc branch=test-doc
	@##
	@##		# Will check "master" if "asdf1234" does not exist.
	@##		make test-doc branch=asdf1234
	@##
	@$(call help,$@:)
	@${MAKE} test-doc-checkout
	@${MAKE} test-doc-install
	@${MAKE} test-doc-build

## Update the local copy of the doc.
test-doc-checkout:
	@$(call help,$@:)
	@[ ! -d doc ] && git clone ${repo} doc || :
	@cd doc && { \
		git reset --hard ; \
		git fetch --all ; \
		[ "$$(git branch --show-current)" != "master" ] && git checkout master || : ; \
		[ "${branch}" != "master" ] \
			&& { \
				{ \
					git branch -D ${branch} 2> /dev/null ; \
					git checkout ${branch} ; \
				} \
					&& git pull --ff-only origin ${branch} \
					|| { \
						>&2 echo "[!] The branch '${branch}' doesn't exist, checking out 'master' instead..." ; \
						git pull --ff-only origin master ; \
					} \
			} \
			|| git pull --ff-only origin master ; \
	} 1> /dev/null

## Install doc dependencies.
test-doc-install:
	@$(call help,$@:)
	@pip install --requirement doc/requirements.txt 1> /dev/null
	@pip install --editable .[dev] --upgrade 1> /dev/null

## Dry-build the doc.
test-doc-build:
	@$(call help,$@:)
	@sphinx-build -M dummy doc/source doc/build -n -q -W

## Serve the openfisca Web API.
api:
	@$(call help,$@:)
	@openfisca serve \
		--country-package openfisca_country_template \
		--extensions openfisca_extension_template

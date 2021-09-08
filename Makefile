doc = sed -n "/^$1/ { x ; p ; } ; s/\#\#/[⚙]/ ; s/\./.../ ; x" ${MAKEFILE_LIST}

## Launch all `openfica` tasks.
all: \
	openfica-clean \
	openfica-check-syntax-errors \
	openfica-check-style \
	openfica-check-types \
	openfica-test \
	;

openfica-%:
	@openfica make.$*

## Install project dependencies.
install:
	@$(call doc,$@:)
	@pip install --upgrade invoke pip twine wheel
	@pip install --editable .[dev] --upgrade --use-deprecated=legacy-resolver

## Install openfisca-core for deployment and publishing.
build: setup.py
	@## This allows us to be sure tests are run against the packaged version
	@## of openfisca-core, the same we put in the hands of users and reusers.
	@$(call doc,$@:)
	@python $? bdist_wheel
	@find dist -name "*.whl" -exec pip install --force-reinstall {}[dev] \;

## Uninstall project dependencies.
uninstall:
	@$(call doc,$@:)
	@pip freeze | grep -v "^-e" | sed "s/@.*//" | xargs pip uninstall -y

#!/usr/bin/make -f

SHELL := /bin/bash

.PHONY: help fmt lint sectest build-docs build-wheel coverage format-python format-toml lint-markdown lint-docstrings lint-python lint-shell lint-workflows lint-yaml security-bandit security-safety test types

export PROJECT_NAME = pi_portal
export GIT_ROOT = $(shell git rev-parse --show-toplevel)

define p
	# Wrapper to run poetry commands without arguments

	# $1 - Command

    poetry_shim $(1)
endef

define p+
	# Wrapper to run poetry commands with argument parsing

	# $1 - Command
	# $2 - Fallback command

	# MAKE_ARGS defined						- Call default command with MAKE_ARGS
	if [[ -n '${MAKE_ARGS}' ]]; then poetry_shim ${1} ${MAKE_ARGS}; fi

	# Fallback command set, no MAKE_ARGS 	- Call fallback command
	if [[ -n '${2}' ]] && [[ -z '${MAKE_ARGS}' ]]; then poetry_shim ${2}; fi

	# No fallback command set, no MAKE_ARGS - Call default command with PROJECT_NAME
	if [[ -z '${2}' ]] && [[ -z '${MAKE_ARGS}' ]]; then poetry_shim ${1} ${PROJECT_NAME}; fi
endef

help:
	@echo "Please use \`dev <target>' where <target> is one of"
	@echo "  build-docs        to build the documentation"
	@echo "  build-wheel       to build the wheel"
	@echo "  coverage          to run coverage"
	@echo "  format-python     to format Python files"
	@echo "  format-toml       to format TOML files"
	@echo "  lint-docstrings   to lint docstrings"
	@echo "  lint-shell        to lint shell scripts"
	@echo "  lint-python       to lint Python files"
	@echo "  lint-workflows    to lint all files"
	@echo "  lint-yaml         to lint YAML files"
	@echo "  security-bandit   to check security practices"
	@echo "  security-safety   to check dependencies"
	@echo "  test              to run tests"
	@echo "  types             to check typing"

fmt: format-python format-toml
lint: lint-docstrings lint-shell lint-yaml lint-python
sectest: security-bandit security-safety

command:
	@make $(MAKE_COMMAND)

build-docs:
	@echo "Building docs ..."
	@rm -rf documentation/codebase/pi_portal/_autosummary
	@$(call p, "cd documentation && make clean && make html")
	@echo "Done."

build-wheel:
	@echo "Building wheel ..."
	@echo "COMMAND: poetry build -f wheel"
	@poetry build -f wheel
	@echo "Done."

coverage:
	@echo "Running coverage ..."
	@$(call p, "coverage run -m pytest && coverage html")
	@echo "Done."

format-python:
	@echo "Formatting all Python files ..."
	@$(call p+, "yapf -i --recursive --verbose --parallel", "yapf -i --recursive --verbose --parallel .")
	@$(call p+, "isort")
	@echo "Done."

format-toml:
	@echo "Formatting all TOML files ..."
	@echo "COMMAND: tomll **/*.toml"
	@find . -type f -name "*.toml" -exec tomll {} \;
	@echo "Done."

lint-docstrings:
	@echo "Checking docstrings ..."
	@$(call p+, "darglint2")
	@$(call p+, "pydocstyle")
	@echo "Done."

lint-shell:
	@echo "Checking all shell scripts ..."
	@echo "COMMAND: shellcheck **/*.sh"
	@shellcheck **/*.sh

	@echo "Done."

lint-python:
	@echo "Checking Python files ..."
	@$(call p+, "isort --check-only --diff")
	@$(call p+, "pylint", "pytest --pylint --pylint-jobs=2 ${PROJECT_NAME}")
	@echo "Done."

lint-yaml:
	@echo "Checking all YAML files ..."
	@$(call p, "yamllint .")
	@echo "Done."

security-bandit:
	@echo "Checking all security code practices ..."
	@$(call p, "bandit -c pyproject.toml -r $(PROJECT_NAME) -x tests")
	@echo "Done."

security-safety:
	@echo "Checking all dependencies ..."
	@$(call p, "pip freeze | safety check --stdin -i 44715 -i 44716 -i 44717")
	@echo "Done."

test:
	@echo "Running tests ..."
	@$(call p+, "pytest")
	@echo "Done."

types:
	@echo "Checking types ..."
	@$(call p+, "mypy --strict --show-error-codes --implicit-reexport --explicit-package-bases")
	@echo "Done."

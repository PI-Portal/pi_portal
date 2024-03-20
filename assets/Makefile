#!/usr/bin/make -f

SHELL := /bin/bash

.PHONY: help clean docker fmt lint md sectest build-docs build-wheel clean-git clean-pycache coverage format-python format-shell format-toml lint-dockerfile lint-docstrings lint-markdown lint-python lint-shell lint-workflows lint-yaml release security-bandit security-leaks security-safety spelling-add spelling-markdown spelling-sync test types

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
	@echo "  clean-git         to run git clean"
	@echo "  clean-pycache     to clean __pycache__ content"
	@echo "  coverage          to run coverage"
	@echo "  format-python     to format Python files"
	@echo "  format-shell      to format shell scripts"
	@echo "  format-toml       to format TOML files"
	@echo "  lint-dockerfile   to lint Dockerfiles"
	@echo "  lint-docstrings   to lint docstrings"
	@echo "  lint-markdown     to lint markdown files"
	@echo "  lint-python       to lint Python files"
	@echo "  lint-shell        to lint shell scripts"
	@echo "  lint-workflows    to lint all files"
	@echo "  lint-yaml         to lint YAML files"
	@echo "  release           to cut a new release"
	@echo "  security-bandit   to check security practices"
	@echo "  security-leaks    to check for credential leaks"
	@echo "  security-safety   to check dependencies"
	@echo "  spelling-add      to add a regex to the ignore patterns"
	@echo "  spelling-markdown to spellcheck markdown files"
	@echo "  spelling-sync     to synchronize vale packages"
	@echo "  test              to run tests"
	@echo "  types             to check typing"

clean: clean-git clean-pycache
docker: lint-dockerfile
fmt: format-python format-shell format-toml
lint: lint-docstrings lint-shell lint-python lint-yaml
md: lint-markdown spelling-markdown
sectest: security-bandit security-leaks security-safety

command:
	@make $(MAKE_COMMAND)

build-docs:
	@echo "Building docs ..."
	@rm -rf documentation/source/codebase/pi_portal/_autosummary
	@$(call p, "cd documentation && make clean && make html")
	@echo "Done."

build-wheel:
	@echo "Building wheel ..."
	@echo "COMMAND: poetry build -f wheel"
	@poetry build -f wheel
	@echo "Done."

clean-git:
	@echo "Cleaning git content ..."
	@git clean -fd
	@echo "Done."

clean-pycache:
	@echo "Cleaning __pycache__ content ..."
	@$(call p, "find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete")
	@echo "Done."

coverage:
	@echo "Running coverage ..."
	@$(call p, "coverage run -m pytest && coverage html || (coverage report; exit 127)")
	@echo "Done."

format-python:
	@echo "Formatting all Python files ..."
	@$(call p+, "pre-commit run yapf --verbose --files", "pre-commit run yapf  --verbose --all-files")
	@$(call p+, "pre-commit run isort --verbose --files", "pre-commit run isort --verbose --all-files")
	@echo "Done."

format-shell:
	@echo "Formatting all shell scripts ..."
	@$(call p+, "pre-commit run format-shell --verbose --files", "pre-commit run format-shell --verbose --all-files")
	@echo "Done."

format-toml:
	@echo "Formatting all TOML files ..."
	@$(call p+, "pre-commit run format-toml --verbose --files", "pre-commit run format-toml --verbose --all-files")
	@echo "Done."

lint-dockerfile:
	@echo "Checking Dockerfiles ..."
	@$(call p+, "pre-commit run lint-dockerfile --verbose --files", "pre-commit run lint-dockerfile --verbose --all-files")
	@echo "Done."

lint-docstrings:
	@echo "Checking docstrings ..."
	@$(call p+, "pre-commit run darglint2 --verbose --files", "pre-commit run darglint2 --verbose --all-files")
	@$(call p+, "pre-commit run pydocstyle --verbose --files", "pre-commit run pydocstyle --verbose --all-files")
	@echo "Done."

lint-markdown:
	@echo "Checking markdown files ..."
	@$(call p+, "pre-commit run lint-markdown --verbose --files", "pre-commit run lint-markdown --verbose --all-files")
	@echo "Done."

lint-shell:
	@echo "Checking all shell scripts ..."
	@$(call p+, "pre-commit run lint-shell --verbose --files", "pre-commit run lint-shell --verbose --all-files")
	@echo "Done."

lint-python:
	@echo "Checking Python files ..."
	@$(call p+, "pre-commit run isort --verbose --files", "pre-commit run isort --verbose --all-files")
	@$(call p+, "pylint", "pytest --pylint -m pylint ${PROJECT_NAME}")
	@echo "Done."

lint-yaml:
	@echo "Checking all YAML files ..."
	@$(call p, "pre-commit run yamllint --verbose --all-files")
	@echo "Done."

release:
	@echo "Creating Release ..."
	@$(call p, "cz bump -s")
	@echo "Done."

security-bandit:
	@echo "Checking all security code practices ..."
	@$(call p, "pre-commit run bandit --verbose --all-files")
	@echo "Done."

security-leaks:
	@echo "Checking all security leaks ..."
	@$(call p, "pre-commit run security-credentials --verbose --all-files")
	@echo "Done."

security-safety:
	@echo "Checking all dependencies ..."
	@$(call p, "pip freeze | safety check --stdin")
	@echo "Done."

spelling-add:
	@echo "Adding word ..."
	@echo "${MAKE_ARGS}" >> ".vale/Vocab/${PROJECT_NAME}/accept.txt"
	@sort -u -o ".vale/Vocab/${PROJECT_NAME}/accept.txt" ".vale/Vocab/${PROJECT_NAME}/accept.txt"

spelling-sync:
	@echo "Synchronizing vale ..."
	@$(call p, "pre-commit run --hook-stage manual spelling-vale-sync --verbose")

spelling-markdown:
	@echo "Checking markdown spelling ..."
	@$(call p, "pre-commit run spelling-markdown --verbose --all-files")
	@echo "Done."

test:
	@echo "Running tests ..."
	@$(call p+, "pytest")
	@echo "Done."

types:
	@echo "Checking types ..."
	@$(call p, "pre-commit run poetry-types-python --verbose --all-files")
	@echo "Done."

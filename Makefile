# https://stackoverflow.com/a/26339924
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

%:
	@:

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | python

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | python --uninstall

#* Installation
.PHONY: install
install:
	poetry install -n --remove-untracked

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: format
fmt format:
	poetry run black --config pyproject.toml $(filter-out $@,$(MAKECMDGOALS))
	poetry run isort --settings-path pyproject.toml $(filter-out $@,$(MAKECMDGOALS))

#* Linting
.PHONY: test
test:
	poetry run pytest -c pyproject.toml tests

.PHONY: check-codestyle
check-codestyle:
	poetry run flake8 --count apiclient_pydantic tests
	poetry run black --diff --check --config pyproject.toml apiclient_pydantic tests
	poetry run isort --diff --check-only --settings-path pyproject.toml apiclient_pydantic tests

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml apiclient_pydantic

.PHONY: check-safety
check-safety:
	poetry check
	poetry run safety check --full-report

.PHONY: lint
lint: check-codestyle mypy check-safety

#* Cleaning
.PHONY: clean
clean:
	find . | grep -E '(.DS_Store|.mypy_cache|__pycache__|\.hypothesis|htmlcov|\.pytest_cache|\.coverage|\.perm|\.cache|\.static|\.py[cod]$$)' | xargs rm -rf

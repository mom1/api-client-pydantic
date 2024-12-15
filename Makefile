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
	poetry install -n --sync

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: format
fmt format:
	poetry run ruff format $(filter-out $@,$(MAKECMDGOALS))

#* Linting
.PHONY: test
test:
	poetry run pytest -c pyproject.toml tests

.PHONY: check-codestyle
check-codestyle:
	poetry run ruff check --exit-non-zero-on-fix $(filter-out $@,$(MAKECMDGOALS))

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml $(filter-out $@,$(MAKECMDGOALS))

.PHONY: lint
lint:
	@$(MAKE) -s check-codestyle $(filter-out $@,$(MAKECMDGOALS))
	@$(MAKE) -s mypy $(filter-out $@,$(MAKECMDGOALS))

#* Cleaning
.PHONY: clean
clean:
	find . | grep -E '(.DS_Store|.mypy_cache|__pycache__|\.hypothesis|htmlcov|\.pytest_cache|\.coverage|\.perm|\.cache|\.static|\.py[cod]$$)' | xargs rm -rf

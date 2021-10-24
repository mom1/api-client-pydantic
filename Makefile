# https://stackoverflow.com/a/26339924
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

%:
	@:

.PHONY: pyclean
pyclean:
	# Cleaning cache
	find . | grep -E '(__pycache__|\.hypothesis|htmlcov|\.pytest_cache|\.coverage|\.perm|\.cache|\.static|\.py[cod]$$)' | xargs rm -rf

.PHONY: install
install:
	poetry install --remove-untracked

.PHONY: test
test:
	poetry run pytest tests

.PHONY: lint
lint:
	poetry run flake8 --count $(filter-out $@,$(MAKECMDGOALS))

.PHONY: format
format:
	poetry run yapf -i $(filter-out $@,$(MAKECMDGOALS))
	poetry run isort $(filter-out $@,$(MAKECMDGOALS))

.PHONY: change
change:
	poetry run gitchangelog


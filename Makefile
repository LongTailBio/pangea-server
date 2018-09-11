.PHONY: clean-pyc clean-build clean lint-app lint-tests lint-seed lint-worker lint-analysis-packages lint test cov
.DEFAULT_GOAL: help

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with pylint"
	@echo "lint-tests - check style of tests with pylint"
	@echo "test - run tests quickly with the default Python"
	@echo "cov - run tests and check coverage with the default Python"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint-app:
	pylint --rcfile=.pylintrc app -f parseable -r n && \
	pycodestyle app --max-line-length=120 && \
	pydocstyle app

lint-tests:
	pylint --rcfile=.pylintrc tests -f parseable -r n && \
	pycodestyle tests --max-line-length=120 && \
	pydocstyle tests

lint-seed:
	pylint --rcfile=.pylintrc seed -f parseable -r n && \
	pycodestyle seed --max-line-length=120 && \
	pydocstyle seed

lint-worker:
	pylint --rcfile=.pylintrc worker -f parseable -r n && \
	pycodestyle worker --max-line-length=120 && \
	pydocstyle worker

lint-analysis-packages:
	pylint --rcfile=.pylintrc analysis_packages -f parseable -r n && \
	pycodestyle analysis_packages --max-line-length=120 && \
	pydocstyle analysis_packages

lint:
	pylint --rcfile=.pylintrc app tests seed worker analysis_packages tool_packages -f parseable -r n && \
	pycodestyle app tests seed worker analysis_packages tool_packages --max-line-length=120 && \
	pydocstyle app tests seed worker analysis_packages tool_packages

test:
	pytest tests analysis_packages tool_packages

cov:
	pytest --cov-report html \
	       --cov-config .coveragerc \
	       --cov=app tests analysis_packages tool_packages

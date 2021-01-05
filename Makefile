FOLDERS:=slackcat tests

do_format:
	isort $(FOLDERS)
	black $(FOLDERS)

format:
	isort -c $(FOLDERS)
	black -c $(FOLDERS)

pylint:
	pylint $(FOLDERS)

flake8:
	flake8 $(FOLDERS)

mypy:
	MYPYPATH=stubs mypy $(FOLDERS)

lint: flake8 pylint mypy

test:
	pytest tests/

check: format lint test

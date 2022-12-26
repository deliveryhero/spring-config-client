.PHONY: tests

VENV := venv

all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

venv: $(VENV)/bin/activate

install: venv
	$(VENV)/bin/pip install -r requirements.txt

tests: venv
	pytest $(flags)

test: venv
	pytest $(flags) -k $(t)

bump: venv
	bumpversion --config-file .bumpversion.cfg minor

build: venv
	python3 -m build

clean:
	rm -rf ./dist
	rm -rf ./sc_utils.egg-info
	rm -rf ./scutils.egg-info

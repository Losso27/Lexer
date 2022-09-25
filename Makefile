VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
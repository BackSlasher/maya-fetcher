.PHONY: run freeze
freeze:
	venv/bin/pip freeze > requirements.txt
run:
	venv/bin/python main.py

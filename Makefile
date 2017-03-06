help:
	@echo "COMMAND: runserver | help"

runserver:
	@webhookit -p 18340 -c tests/config.py

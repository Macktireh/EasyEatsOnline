.PHONY: run m u mu sm shell test superuser black isort ruff clean

.DEFAULT_GOAL := run

run:
	poetry run flask run

# migrate
m:
	poetry run python flask migrate

# makemigrations
u:
	poetry run flask upgrade

# migrate + upgrade
mu: m u

# showmigrations
sm:
	poetry run flask show

shell:
	poetry run flask shell

testc:
	coverage run -m unittest discover tests/ -v

coverage:
	coverage report -m
	coverage html

test: testc coverage

superuser:
	poetry run flask createsuperuser

black:
	poetry run python -m black .

isort:
	poetry run python -m isort --profile black .

ruff:
	poetry run ruff check .

# clean
clean: black isort ruff

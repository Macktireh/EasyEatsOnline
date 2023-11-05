.PHONY: run m u mu sm shell test superuser rufffix ruffformat ruff clean

.DEFAULT_GOAL := run

run:
	poetry run flask run

m:
	poetry run python flask db migrate

u:
	poetry run flask db upgrade

# migrate + upgrade
mu: m u

# showmigrations
sm:
	poetry run flask db show

shell:
	poetry run flask shell

testc:
	poetry run coverage run -m unittest discover tests/ -v

coverage:
	poetry run coverage report -m
	poetry run coverage html

test: testc coverage

superuser:
	poetry run flask createsuperuser

rufffix:
	poetry run ruff --fix --exit-zero .

ruffformat:
	poetry run ruff format .

ruff:
	poetry run ruff check .

clean: rufffix ruffformat ruff

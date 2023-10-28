.PHONY: runserver m mm mmm sm shell test superuser loaddata dumpdata i18n

.DEFAULT_GOAL := runserver

runserver:
	poetry run python manage.py runserver

# migrate
m:
	poetry run python manage.py migrate

# makemigrations
mm:
	poetry run python manage.py makemigrations

# makemigrations + migrate
mmm: mm m

# showmigrations
sm:
	poetry run python manage.py showmigrations

shell:
	poetry run python manage.py shell_plus

testc:
	coverage run -m unittest discover tests/ -v

coverage:
	coverage report -m
	coverage html

test: testc coverage

superuser:
	poetry run python manage.py createsuperuser --email=admin@gmail.com --name=Admin --phone_number=77123456

loaddata:
	poetry run python manage.py load_data

dumpdata:
	poetry run python manage.py dumpdata > db.json

i18n:
	poetry run django-admin makemessages --all --ignore=env

black:
	poetry run python -m black .

isort:
	poetry run python -m isort --profile black .

ruff:
	poetry run ruff check .

# clean
clean: black isort ruff

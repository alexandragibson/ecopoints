start:
	python manage.py runserver

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

test:
	python manage.py test

collectstatic:
	python manage.py collectstatic

compress:
	python manage.py compress --force

populate:
	python ./populate_ecopoints.py

coverage:
	coverage run --source='.' manage.py test ecopoints.tests
	coverage report -m # -m shows line where coverage is missing

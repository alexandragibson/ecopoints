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

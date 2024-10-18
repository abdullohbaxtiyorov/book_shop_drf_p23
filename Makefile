mig:
	python manage.py makemigrations
	python manage.py migrate

load:
	python manage.py loaddata country

celery:
	celery -A root worker -l INFO

delmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

flush:
	python3 manage.py flush

load_data:
	python3 manage.py loaddata country

user:
	python3 manage.py createsuperuser --email admin@gmail.com
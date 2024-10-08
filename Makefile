.PHONY: up down build migrate createsuperuser run

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	python manage.py makemigrations
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser --noinput || true

run:
	python manage.py runserver 0.0.0.0:8000
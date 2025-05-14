build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

collectstatic:
	python3 manage.py collectstatic

migrate:
	python3 manage.py makemigrations

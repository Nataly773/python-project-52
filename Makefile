install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

update_lang:
	uv run django-admin makemessages -l ru

compile_lang:
	uv run django-admin compilemessages

start-server:
	uv run python3 manage.py runserver

lint:
	uv run ruff check task_manager

migrate:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

collectstatic:
	uv run python3 manage.py collectstatic --no-input

test:
	uv run python3 manage.py test
run:
	uv sync
	cd app && python manage.py migrate \
	&& uv run main.py

mm:
	cd app && python manage.py makemigrations
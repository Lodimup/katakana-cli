run:
	uv sync
	cd app && python manage.py migrate \
	&& python main.py

mm:
	cd app && python manage.py makemigrations
build:
	docker-compose up -d --build
	docker exec -it room_reservations_django_1 bash

container:
	docker exec -it room_reservations_django_1 bash

test:
	DJANGO_SETTINGS_MODULE=reservations.settings.test pytest $(TEST_ME_PLEASE)

shell:
	./manage.py shell_plus

run:
	./manage.py runserver 0:8000

makemigrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

build:
	docker-compose up -d --build
	docker exec -it room_reservations_django_1 bash

container:
	docker exec -it room_reservations_django_1 bash

test:
	./manage.py test $(TEST_ME_PLEASE) --settings=reservations.settings.test

shell:
	./manage.py shell_plus

run:
	./manage.py runserver 0:8000

makemigrations:
	./manage.py makemigrations

migrate:
	./manage.py migrate

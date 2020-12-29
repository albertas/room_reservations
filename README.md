Usage
=====
- Install `docker` and `docker-compose`.
- Clone this project by running `git clone https://github.com/albertas/room_reservations/`
- Build, start and attach to docker container by running `make build` in the root directory of this project.
- Run the tests `make test` to see if everything works fine.
- Execute migrations by running `make migrate`
- Create super user by running `./manage.py createsuperuser`
- Run the development server by running `make run` and open `http://localhost:8000` to browser swagger UI page,
  which can be used to call REST API endpoints.
- Login with superuser you just created to engage with API endpoints. Don't forget to click "Try it out" button to be able to execute API queries.

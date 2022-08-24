download-models:
	tools/download-models.sh

install-client:
	poetry install --extras client

install-service:
	poetry install --extras service

setup-raspberry:
	scp raspberry/setup.sh pi@raspberrypi.local:.
	ssh pi@raspberrypi.local 'bash setup.sh -b'

start-client:
	poetry run start-client

start-service:
	poetry run start-service

start-service-dev:
	poetry run start-service-dev

test:
	poetry run pytest

test-watch:
	poetry run ptw

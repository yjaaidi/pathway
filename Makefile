download-models:
	tools/download-models.sh

install:
	poetry install

setup-raspberry:
	scp raspberry/setup.sh pi@raspberrypi.local:.
	ssh pi@raspberrypi.local 'bash setup.sh -b'

start:
	poetry run start

start-dev:
	poetry run start-dev

test:
	poetry run pytest

test-watch:
	poetry run ptw

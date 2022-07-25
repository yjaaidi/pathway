download-models:
	tools/download-models.sh

install:
	echo "Creating conda env if not exists..."
	conda env list | grep pathway || conda create -n pathway
	echo "Updating env..."
	conda env update -n pathway --file environment.yml

setup-raspberry:
	scp raspberry/setup.sh pi@raspberrypi.local:.
	ssh pi@raspberrypi.local 'bash setup.sh -b'

start:
	./main.py

test:
	pytest

test-watch:
	ptw


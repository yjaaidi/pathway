install:
	echo "Creating conda env if not exists..."
	conda env list | grep pathway || conda create -n pathway
	echo "Updating env..."
	conda env update -n pathway --file environment.yml

start:
	./main.py

setup-raspberry:
	scp raspberry/setup.sh pi@raspberrypi.local:.
	ssh pi@raspberrypi.local 'bash setup.sh -b'

test:
	pytest

test-watch:
	ptw

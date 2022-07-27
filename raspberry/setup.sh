#!/usr/bin/env ssh

set -e
set -x

echo "Enabling mDNS discovery"
echo "<service-group>
 <name replace-wildcards=\"yes\">%h SSH</name>
  <service>
   <type>_ssh._tcp</type>
   <port>22</port>
  </service>
</service-group>" | sudo tee /etc/avahi/services/ssh.service

echo "APT Update"
sudo apt-get update

echo "Installing required libraries"
# Fixes missing libGL.so.1
sudo apt install -y libgl1-mesa-glx

echo "Installing picamera2 dependencies"
sudo apt install -y python3-libcamera python3-kms++
sudo apt install -y python3-prctl libatlas-base-dev ffmpeg libopenjp2-7
NOGUI=1 pip3 install git+https://github.com/raspberrypi/picamera2.git

# Poetry 1.2.0a install didn't work
# in order to use virtualenvs.options.system-site-packages
# that is why we are hacking our way and forcing system import.
echo "Setting PYTHONPATH to include picamera2"
echo 'export PYTHONPATH=/home/pi/.local/lib/python3.9/site-packages:$PYTHONPATH' >> ~/.bashrc

echo "Installing pip & venv"
sudo apt-get install -y python3-pip python3-venv

echo "Setting up poetry"
curl -sSL https://install.python-poetry.org | python -
source ~/.bashrc

echo "Installing git"
sudo apt-get install -y git

echo "Cloning source code"
git clone https://github.com/yjaaidi/pathway.git

echo "Go into source code directory"
cd pathway

echo "Pathway > Installing"
make install

echo "Pathway > Downloading models"
make download-models

echo "Reboot"
sudo reboot

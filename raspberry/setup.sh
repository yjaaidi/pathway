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

echo "Installing Python 3"
sudo apt-get install -y python3-pip

echo "Installing required libraries"
# Fixes missing libGL.so.1
sudo apt install -y libgl1-mesa-glx

echo "Setting up poetry"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source ~/.bashrc
poetry config virtualenvs.in-project true

echo "Installing git"
sudo apt-get install -y git

echo "Cloning source code"
git clone https://github.com/yjaaidi/pathway.git

echo "Go into source code directory"
cd pathway

echo "Pathway > Installing"
make install

echo "Reboot"
sudo reboot

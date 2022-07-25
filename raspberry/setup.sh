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

echo "Installing miniconda"
wget https://github.com/conda-forge/miniforge/releases/download/4.13.0-0/Miniforge3-4.13.0-0-Linux-aarch64.sh -O install-miniforge.sh
chmod u+x install-miniforge.sh
./install-miniforge.sh
miniforge3/bin/conda init bash
source ~/.bashrc

echo "Installing git"
sudo apt-get install -y git

echo "Cloning source code"
git clone https://github.com/yjaaidi/pathway.git

echo "Go into source code directory"
cd pathway

echo "Pathway > Installing"
make install

# echo "Installing Python 3"
# sudo apt-get install python3-pip

# sudo reboot

# Fixes numpy install
# apt-get install libatlas-base-dev

# pip install -r requirements-src.txt
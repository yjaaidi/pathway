# Setup

```sh
conda create -n pathway -f environment.yml
./download-models.sh
./main.py
```

# Adding dependencies

```sh
./install.sh [dependency ...] 
```

# Set up raspberry

```sh
./setup-raspberry.sh
```

# Connect to Raspberry

```sh
ssh pi@raspberrypi.local
```

or `nmap -p 22 192.168.xxx.0/24`
or `dns-sd -Gv4 raspberrypi.local` to grab the IP address

# Setup

```sh
make install
make download-models
make start
```

# Adding dependencies

```sh
tools/install.sh [dependency ...] 
```

# Set up raspberry

```sh
make setup-raspberry
```

# Connect to Raspberry

```sh
ssh pi@raspberrypi.local
```

or `nmap -p 22 192.168.xxx.0/24`
or `dns-sd -Gv4 raspberrypi.local` to grab the IP address

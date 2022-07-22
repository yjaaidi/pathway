# Setup

```sh
conda create -n pathway -f environment.yml
./download-models.sh
./main.py
```

# Update environment.yml

```sh
conda env export -n pathway > environment.yml
```
# pypride-dev

## Installation

```bash
pip install git+https://github.com/dmitryduev/pypride.git
```

## build and run with `docker`

```bash
docker build --rm -t pypride:latest -f Dockerfile .
docker run -it --rm --name pypride pypride:latest
#docker run -it --rm --name pypride -v /path/to/data:/data pypride:latest
```
Fetch and clip DE430:

```bash
pip install jplephem
wget -O de430.full.bsp http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp
python -m jplephem excerpt 2000/1/1 2050/1/1 de430.full.bsp de430.bsp

wget -O de421.full.bsp http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp
python -m jplephem excerpt 2000/1/1 2050/1/1 de421.full.bsp de421.bsp
```
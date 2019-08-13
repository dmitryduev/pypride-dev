```bash
wget http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp
python -m jplephem excerpt 2000/1/1 2050/1/1 de430.bsp de430.clipped.bsp
```
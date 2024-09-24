# Solar-Sim

![overview](https://user-images.githubusercontent.com/73968949/146631939-b9c9aebc-1b62-4b26-b603-0a33e2753a76.png)

Simple simulation of major bodies of the solar system using Euler's method, including the 8 planets and several moons. 

This project was created with 2 other people for a physics class. Most of the programming was my job, except for the controls.

Position and velocity data is grabbed at runtime from JPL Horizons. The initial position and velocities of all the simulated bodies are at the accurate positions from January 1, 2020. Of course, error accumulates over time, and the simulation becomes less accurate to reality as it runs, especially when ran at a faster speed.

Masses of the planets and moons cannot be queried from JPL Horizons, so I added them manually.

These dependencies need to be installed to run `main.py` above:
* Astroquery: Instructions at https://github.com/astropy/astroquery
* VPython: You can just `pip install vpython`

Controls:\
Up Arrow - Make time pass 1.5x faster\
Down Arrow - Make time pass 1.5x slower

Right Arrow - Follow Next Body\
Left Arrow - Follow Previous Body

Right click the mouse to rotate around the body you are currently focused on. Use the mouse wheel to zoom.

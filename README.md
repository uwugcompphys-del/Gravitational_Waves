# Gravitational Waves Project
This project simulates the spatial gravitational strain tensor $h_{ij}$ from various astrophysical sources over coordinate time. The current implementation includes a spinning neutron star. 

## Theoretical Background

## Gravitational Waves
The actual strain tensor itself is calculated in the file `grav_waves.py`

## Celestial Objects
The sources of the gravitational waves are stored as classes in the file `celestical_objects.py`

## Rotations
A source needs to undergo motion in order for gravitational waves to be emitted. If a source is spinning, the equations of rotational motion can be extracted from the `rotations.py` file for use

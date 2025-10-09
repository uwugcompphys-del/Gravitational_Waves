# Gravitational Waves Project
This project is a work in progress. The readme and the rest of the project is corrently incomplete. simulates the spatial gravitational strain tensor $h_{ij}$ from various astrophysical sources over coordinate time. The current implementation includes a spinning neutron star. The system of units is $c=G=km=1$. As a result, the unit of time is a half-week.

## Theoretical Background
The current implementation assumes that the source is sufficiently far away such that the backgorund metric is equal to the Minkowski metric. With this approximation, we use corrdinate time and evaluate only the spatial components. Hence the resultant metric can be expressed as $g_{\mu\nu}\approx \eta_{\mu\nu}+h_{\mu\nu}$ Where $h_{\mu\nu}$ is a small perturbation known as the "Strain Tensor" due to the source of gravitational waves. 
And the strain tensor is found by the following

$$h_{ij}=\frac{2Q_{ij}}{d}$$
Where $d$ is the distance from the source and $Q_{ij}$ is the mass quadrupole moment of the source found by 
$$Q_{ij}=M(3x_ix_j-|x|^2\delta_{ij})$$


## Gravitational Waves
The actual strain tensor itself is calculated in the file `grav_waves.py`

## Celestial Objects
The sources of the gravitational waves are stored as classes in the file `celestical_objects.py`. Currently there is only a neutron star object in the file. 

## Rotations
A source needs to undergo motion in order for gravitational waves to be emitted. If a source has a component of rotational motion, the equations of rotational motion can be extracted from the `rotations.py` file for use

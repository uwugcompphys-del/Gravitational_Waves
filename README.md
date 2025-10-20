# Gravitational Waves Project
This project is a work in progress. The readme and the rest of the project is currently incomplete. simulates the spatial gravitational strain tensor $h_{ij}$ from various astrophysical sources over coordinate time. The current implementation includes a spinning neutron star. The system of units is $c=G=1$.

## Theoretical Background
The current implementation assumes that the source is sufficiently far away such that the background metric is equal to the Minkowski metric. With this approximation, we use corrdinate time and evaluate only the spatial components. Hence the resultant metric can be expressed as $g_{\mu\nu}\approx \eta_{\mu\nu}+h_{\mu\nu}$ Where $h_{\mu\nu}$ is a small perturbation known as the "Strain Tensor" due to the source of gravitational waves. 
The strain tensor and the associated mass quadrupole moment is found by the Einstein Quadrupole Formula.

$$h_{ij}=\frac{2}{r}\ddot{Q_{ij}}(t-r)$$

We start the simulation at the time the first gravitational wave first reaches the observer. In other words, we perform the shift $t\to t+r$. Hence the formula becomes

$$h_{ij}=\frac{2}{r}\ddot{Q_{ij}}(t)$$

Where $d$ is the distance from the source and $Q_{ij}$ is the mass quadrupole moment of the source found by 

$$Q_{ij}=\int_V\rho(\vec{x})(x_ix_j-\frac{1}{3}|\vec{x}|^2\delta_{ij})\ dV$$


## Gravitational Waves
The actual strain tensor itself is calculated in the file `grav_waves.py`

## Celestial Objects
The sources of the gravitational waves are stored as classes in the file `celestial_objects.py`. Currently there is only a neutron star object in the file. 

## Rotations
A source needs to undergo motion in order for gravitational waves to be emitted. If a source has a component of rotational motion, the equations of rotational motion can be extracted from the `rotations.py` file for use

## Fourier Analysis
The frequencies of the generated gravitational waves can be extracted via Fourier Transform. This is done with `fourierAnalysis.py`

## Saving Gravitational Waves
Gravitational Wave files can be saved using `grav_waves.strain_writer()` and must be stored in the `strain_tensors` folder 

## Running Functions
Run functions in the `run_commands_here.py` file by first importing the relevant files and calling the function inside the `run_commands_here.py` file. Do not call 
functions inside the file where the function is defined (Or comment out the calls when pushing to GitHub). 

## Dependnecies
This project requires the following dependencies to run: `numpy`, `scipy`, `matplotlib`

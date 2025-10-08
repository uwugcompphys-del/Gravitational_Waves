import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt 
import densities

#create theta(t, omega0) functions for use in the rotation tensors in rotations.py

def constant(t, omega0=1):
    return omega0

def accelerating(t, omega0=1):
    return omega0*t+t**2

def oscillating(t, omega0=1):
    return omega0*(1+np.sin(2*t)/5)

def linear_decreasing(t, omega0=1):
    return omega0*(1-t*10e-6)

def linear_decrease_precession(t, omega0=1):
    precession_angle = 0.5 * np.sin(np.pi * t)
    return omega0 * (1 - 1e-5 * t) + precession_angle
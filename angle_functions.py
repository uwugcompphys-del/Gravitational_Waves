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
    return omega0*t*(1+np.sin(2*t)/5)

def linear_decreasing(t, omega0=1):
    return omega0*t*(1-10e-6)

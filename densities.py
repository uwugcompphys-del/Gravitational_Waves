import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt 


"""
This file contains density profiles for use in objects. Use (z,y,x) convention since scipy integrate likes it.
"""

def const(z, y, x, rho0,a,b,c):
    """
    Return the density profile of an object with uniform mass
    """
    return rho0

def neutron_star_gaussian_approx(z, y, x, rho0,a,b,c):
    """
    Return the density profile of the object, approxima6ting the polytropic profile (the polytropic profile is too slow)
    """
    r_squared_scaled=(x/a)**2 + (y/b)**2 + (z/c)**2
    return rho0*np.exp(-r_squared_scaled**2)

def near_circular_neutron_star(z,y,x,rho0,a,b,c):
    """
    Return a polytrope-like density profile for a neutron star. THIS IS VERY SLOW.
    """
    r_squared = x**2+y**2+z**2
    R_squared = np.average([a,b,c])**2
    if r_squared<R_squared:
        return np.sqrt(1-r_squared/R_squared)
    else: 
        return 0
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt 
import densities
import angle_functions

#TThis is where the most commonly used rotation tensors are stored
 
def not_rotating(t, omega0=1):
    return np.eye(3)


#Can customise rotation rate with lambda function (example if omega0=t^2 then can use lambda to do lambda t:t**2)
def z_const_rotation(t, omega0=1):
    """
    Rotate at a constant rate omega0 about the z-axis
    """
    theta=omega0*t
    matrix = [
        np.array([np.cos(theta), -np.sin(theta), 0]), 
        np.array([np.sin(theta), np.cos(theta), 0]),
        np.array([0, 0, 1])
    ]
    return np.array(matrix)

def x_const_rotation(t, omega0=1):
    """
    Rotate at a constant rate omega0 about the x-axis
    """
    theta = omega0 * t
    matrix = [
        np.array([1, 0, 0]),
        np.array([0, np.cos(theta), -np.sin(theta)]),
        np.array([0, np.sin(theta), np.cos(theta)])
    ]
    return np.array(matrix)


def y_const_rotation(t, omega0=1):
    """
    Rotate at a constant rate omega0 about the y-axis
    """
    theta = omega0 * t
    matrix = [
        np.array([np.cos(theta), 0, np.sin(theta)]),
        np.array([0, 1, 0]),
        np.array([-np.sin(theta), 0, np.cos(theta)])
    ]
    return np.array(matrix)

def arbitrary_axis_rotation(t, omega0=1):
    """
    Rotate at a constant rate omega0 about an arbitrary axis (the axis is hardcoded to be u in code. Change it manually if want to change axis)
    """
    u_notNorm=np.array([1,1,1]) #Arbitrary axis u, change this in file if want to change the axis of rotation
    u= u_notNorm/np.linalg.norm(u_notNorm)
    theta = omega0 * t
    u = np.asarray(u)
    ux, uy, uz = u

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    R = np.array([
        [ux*ux*one_minus_cos + cos_theta,    ux*uy*one_minus_cos - uz*sin_theta, ux*uz*one_minus_cos + uy*sin_theta],
        [ux*uy*one_minus_cos + uz*sin_theta, uy*uy*one_minus_cos + cos_theta,    uy*uz*one_minus_cos - ux*sin_theta],
        [ux*uz*one_minus_cos - uy*sin_theta, uy*uz*one_minus_cos + ux*sin_theta, uz*uz*one_minus_cos + cos_theta]
    ])

    return R


#For the non constant rotation rate code, need to manually switch out the desired functions

def z_nonConst_rotation(t, omega0=1):
    """
    Rotate at a non-constant rate about the z-axis
    The angle equations are contained in angle_functions.py and is hardcoded into the code as theta=..., if need to change angle equations, manually change 
    the assignment of theta to the desired function.
    """
    theta=angle_functions.linear_decreasing(t,omega0)
    matrix = [
        np.array([np.cos(theta), -np.sin(theta), 0]), 
        np.array([np.sin(theta), np.cos(theta), 0]),
        np.array([0, 0, 1])
    ]
    return np.array(matrix)


def arbitrary_axis_nonConst_rotation_linear_decreasing_rate(t, omega0=1):
    """
    Rotate at a non-constant rate about an arbitrary axis (the axis is hardcoded to be u in code. Change it manually if want to change axis)
    The angle equations are contained in angle_functions.py and is hardcoded into the code as theta=..., if need to change angle equations, manually change 
    the assignment of theta to the desired function.
    """
    u_notNorm=np.array([1,1, 1]) #Arbitrary axis u, change this in file if want to change the axis of rotation
    u= u_notNorm/np.linalg.norm(u_notNorm)
    theta = angle_functions.linear_decrease_precession(t,omega0)
    u = np.asarray(u)
    ux, uy, uz = u

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    R = np.array([
        [ux*ux*one_minus_cos + cos_theta,    ux*uy*one_minus_cos - uz*sin_theta, ux*uz*one_minus_cos + uy*sin_theta],
        [ux*uy*one_minus_cos + uz*sin_theta, uy*uy*one_minus_cos + cos_theta,    uy*uz*one_minus_cos - ux*sin_theta],
        [ux*uz*one_minus_cos - uy*sin_theta, uy*uz*one_minus_cos + ux*sin_theta, uz*uz*one_minus_cos + cos_theta]
    ])

    return R

def arbitrary_precessing_axis_nonConst_rotation_linear_decreasing_rate(t, omega0=1):
    """
    Rotate at a non-constant rate about an arbitrary axis (the axis is hardcoded to be u in code. Change it manually if want to change axis)
    The angle equations are contained in angle_functions.py and is hardcoded into the code as theta=..., if need to change angle equations, manually change 
    the assignment of theta to the desired function.
    """
    u_notNorm=np.array([0.5 * np.cos(np.pi * t),0.5 * np.sin(np.pi * t), 1]) #Arbitrary axis u, change this in file if want to change the axis of rotation
    u= u_notNorm/np.linalg.norm(u_notNorm)
    theta = angle_functions.linear_decrease_precession(t,omega0)
    u = np.asarray(u)
    ux, uy, uz = u

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    R = np.array([
        [ux*ux*one_minus_cos + cos_theta,    ux*uy*one_minus_cos - uz*sin_theta, ux*uz*one_minus_cos + uy*sin_theta],
        [ux*uy*one_minus_cos + uz*sin_theta, uy*uy*one_minus_cos + cos_theta,    uy*uz*one_minus_cos - ux*sin_theta],
        [ux*uz*one_minus_cos - uy*sin_theta, uy*uz*one_minus_cos + ux*sin_theta, uz*uz*one_minus_cos + cos_theta]
    ])

    return R

def arbitrary_LARGE_PRECESSION_axis_nonConst_rotation_linear_decreasing_rate(t, omega0=1):
    """
    Rotate at a non-constant rate about an arbitrary axis (the axis is hardcoded to be u in code. Change it manually if want to change axis)
    The angle equations are contained in angle_functions.py and is hardcoded into the code as theta=..., if need to change angle equations, manually change 
    the assignment of theta to the desired function.
    """
    u_notNorm=np.array([3 * np.cos(2*np.pi * t),3 * np.sin(2*np.pi * t), 1]) #Arbitrary axis u, change this in file if want to change the axis of rotation
    u= u_notNorm/np.linalg.norm(u_notNorm)
    theta = angle_functions.linear_decrease_precession(t,omega0)
    u = np.asarray(u)
    ux, uy, uz = u

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    one_minus_cos = 1 - cos_theta

    R = np.array([
        [ux*ux*one_minus_cos + cos_theta,    ux*uy*one_minus_cos - uz*sin_theta, ux*uz*one_minus_cos + uy*sin_theta],
        [ux*uy*one_minus_cos + uz*sin_theta, uy*uy*one_minus_cos + cos_theta,    uy*uz*one_minus_cos - ux*sin_theta],
        [ux*uz*one_minus_cos - uy*sin_theta, uy*uz*one_minus_cos + ux*sin_theta, uz*uz*one_minus_cos + cos_theta]
    ])

    return R

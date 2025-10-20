import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt 
import densities
import rotations
import celestial_objects 
import time 
import csv 

#Note that c=G=km=1 (time unit: arb. u)
#suggested neutron star rho0: 0.5-1.5
plt.rcParams['font.family'] = 'Times New Roman'
plt.style.use('default') 


def quadrupoles(source, t0, tmax, dt, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating):
    """
    Return the quadrupole tensors of a given source from time t0 to tmax
    Note that sourcemust be a class in celestial_objects
    """
    print("Initialising quadrupole solver...")
    t=t0
    quadTensors=[]
    print("Creating first instance of object")
    while t<=tmax:
        obj = source(t, a, b,c, rho0, density, omega0, rotation)
        obj.quadrupole_Moment()
        quadTensors.append((t, obj.quadMom_tensor)) #Store both the time and the tensor
        print(30*"\n","Computing quadrupole tensors...")
        print(f" Current simulation time: t={t} || Maximum simulation time: tmax={tmax} || {round((t/tmax)*10000)/100}% Complete")
        t+=dt
    print(30*"\n","Computing quadrupole tensors...")
    print(f" Current simulation time: t={tmax} || Maximum simulation time: tmax={tmax} || {round((tmax/tmax)*10000)/100}% Complete")
    print("Quadrupole Calculations complete. ")
    return quadTensors

def ddot_quadrupoles(source, t0, tmax, dt, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating):
    """
    Return the second derivative of the quadrupole tensor
    """
    tensors=quadrupoles(source, t0, tmax, dt, a, b, c, rho0, density, omega0, rotation)
    i = 1 
    print("Computing derivatives...")
    ddot_quad=[]
    while i< len(tensors)-1:
        delta2_Q = tensors[i+1][1]-2*tensors[i][1]+tensors[i-1][1]
        ddot_quad.append((tensors[i][0], delta2_Q/dt**2)) #t=0 is set to be when the first wave is detected => no need to retard time
        i+=1
    print("Derivatives calculated.")
    return ddot_quad

def grav_strain(source, dist, t0, tmax, dt, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating):
    """
    Return the gravitational wave strain caused a given source (a distance dist away from observer) from time t0 to tmax
    Note that sourcemust be a class in celestial_objects
    """
    ddot_quad = ddot_quadrupoles(source, t0, tmax, dt, a, b, c, rho0, density, omega0, rotation)
    print("Computing Gravitational Wave Strain...")
    new_ddot_quad = []
    for tup in ddot_quad:
        new_ddot_quad.append((tup[0], 2*tup[1]/dist))
    print("Strains calculated.")
    return new_ddot_quad


def strain_plotter(source, dist, t0, tmax, dt, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating):
    """
    Plot the diagonal gravitational strain terms (representing expansion)
    """
    tups = grav_strain(source, dist, t0, tmax, dt, a, b, c, rho0, density, omega0, rotation)
    times=[]
    x_expansion=[]
    y_expansion=[]
    z_expansion=[]
    xy_shear=[]
    xz_shear=[]
    yz_shear=[]
    for tup in tups:
        times.append(tup[0])
        x_expansion.append(tup[1][0][0])
        y_expansion.append(tup[1][1][1])
        z_expansion.append(tup[1][2][2])
        xy_shear.append(tup[1][0][1])
        xz_shear.append(tup[1][0][2])
        yz_shear.append(tup[1][1][2])

    print("Solving complete. Plotting results...")
    f, axs = plt.subplots(3,2,figsize=((12,10)))
    axs=axs.flatten()
    f.suptitle("Expansion and Shear Components of the Gravitational Wave Strain Tensor over time")
    plt.style.use('default') 


    instance = source(tmax, a, b, c, rho0, density, omega0, rotation)
    instance.mass()
    instance.quadrupole_Moment()

    axs[0].plot(times,x_expansion, color = "black")
    axs[0].set_xlabel("time after first wave detected (arb. u)")
    axs[0].set_ylabel("h_xx, x-expansion")

    axs[2].plot(times,y_expansion, color = "black")
    axs[2].set_xlabel("time after first wave detected (arb. u)")
    axs[2].set_ylabel("h_yy, y-expansion")
    
    axs[4].plot(times,z_expansion, color = "black")
    axs[4].set_xlabel("time after first wave detected (arb. u)")
    axs[4].set_ylabel("h_zz, z-expansion (1)")

    axs[1].plot(times,xy_shear, color = "black")
    axs[1].set_xlabel("time after first wave detected (arb. u)")
    axs[1].set_ylabel("h_xy, xy-shear")

    axs[3].plot(times,xz_shear, color = "black")
    axs[3].set_xlabel("time after first wave detected (arb. u)")
    axs[3].set_ylabel("h_xz, xz-shear")

    axs[5].plot(times,yz_shear, color = "black")
    axs[5].set_xlabel("time after first wave detected (arb. u)")
    axs[5].set_ylabel("h_yz, yz-shear")

    print("Plotting complete. See output plot for results.")
    print("\n\nSimulation Object Summary")

    print(repr(instance))
    plt.tight_layout()
    plt.show()

def plot_from_file(filepath):
    times=[]
    h_xx = []
    h_yy =[]
    h_zz =[]
    h_xy = []
    h_xz = []
    h_yz = []
    with open(filepath, "r") as file:
        file=csv.DictReader(file)
        for line in file:
            times.append(float(line["time"]))
            h_xx.append(float(line["h_xx"]))
            h_yy.append(float(line["h_yy"]))
            h_zz.append(float(line["h_zz"]))
            h_xy.append(float(line["h_xy"]))
            h_xz.append(float(line["h_xz"]))
            h_yz.append(float(line["h_yz"]))
    f, axs = plt.subplots(3,2,figsize=((12,10)))
    plt.style.use('default') 

    axs=axs.flatten()
    f.suptitle("Expansion and Shear Components of the Gravitational Wave Strain Tensor over time")
    

    axs[0].plot(times,h_xx, color = "black")
    axs[0].set_xlabel("time after first wave detected (arb. u)")
    axs[0].set_ylabel("h_xx, x-expansion")

    axs[2].plot(times,h_yy, color = "black")
    axs[2].set_xlabel("time after first wave detected (arb. u)")
    axs[2].set_ylabel("h_yy, y-expansion")
    
    axs[4].plot(times,h_zz, color = "black")
    axs[4].set_xlabel("time after first wave detected (arb. u)")
    axs[4].set_ylabel("h_zz, z-expansion (1)")

    axs[1].plot(times,h_xy, color = "black")
    axs[1].set_xlabel("time after first wave detected (arb. u)")
    axs[1].set_ylabel("h_xy, xy-shear")

    axs[3].plot(times,h_xz, color = "black")
    axs[3].set_xlabel("time after first wave detected (arb. u)")
    axs[3].set_ylabel("h_xz, xz-shear")

    axs[5].plot(times,h_yz, color = "black")
    axs[5].set_xlabel("time after first wave detected (arb. u)")
    axs[5].set_ylabel("h_yz, yz-shear")

    print("Plotting complete. See output plot for results.")

    plt.tight_layout()
    plt.show()
    

def strain_writer(filepath, tups):
    """
    Write the times and strain tensors stored in tups to a file with path filepath
    """
    print("Writing strain to file")
    with open(filepath,"w") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "h_xx", "h_yy", "h_zz", "h_xy", "h_xz", "h_yz"])
        for t, tensor in tups: 
            row = [t, tensor[0,0], tensor[1][1], tensor[2][2], tensor[0][1], tensor[0][2], tensor[1][2]]
            writer.writerow(row)
    print("Strains successfully written to file with path ", filepath)




#Testing Region
def quadrupole_tester():
    for line in (quadrupoles(celestial_objects.ellipsoid_object,1,2,.1, 1, 1, 1, 1, densities.const, 1, rotations.not_rotating)):
        print(line)


def ddot_quadrupole_tester():
    for line in (ddot_quadrupoles(celestial_objects.ellipsoid_object,1,2,.1, 1, 2, 1, 1, densities.const, 1, rotations.z_const_rotation)):
        print(line)

def wave_strain_tester():
    for line in (grav_strain(celestial_objects.ellipsoid_object,1,0,1,.05, 1, 2, 1, 1, densities.const, 1, rotations.arbitrary_axis_nonConst_rotation_linear_decreasing_rate)):
        print(f"\n\nGravitational Strain at time t={line[0]}:\n")
        for row in line[1]:
            print(row)




    
#quadrupole_tester()
#ddot_quadrupole_tester()
#wave_strain_tester()
#Set distance to be around 1e15 to 1e20
#strain_plotter(celestial_objects.ellipsoid_object,10e10,0,.3,.2, .9, .95, .9, 1, densities.neutron_star_gaussian_approx, 5e4, rotations.arbitrary_axis_nonConst_rotation_linear_decreasing_rate)    
#strain_plotter(celestial_objects.ellipsoid_object,10e10,0,.9,.001, .9, .95, .9, 1, densities.gaussian, 5e4, rotations.arbitrary_axis_neutron_star_rotation)    
#strain_plotter(celestial_objects.ellipsoid_object,5e20,0,30,.01, .95, .9, 1, .8, densities.neutron_star_gaussian_approx, 6, rotations.arbitrary_precessing_axis_const_rotation_rate) #change timestep back to .05 if not have a lot of time


#strainTensor = grav_waves.grav_strain(celestial_objects.ellipsoid_object, 1e16, 0, 30, 0.01, 1, 0.95, 1.05, .8, densities.neutron_star_gaussian_approx, 10, rotations.arbitrary_precessing_axis_const_rotation_rate)

#strain_filepath = "/Users/kanlachlan/Documents/VS_Code/Personal Projects/Gravitational_Waves/strain_tensors/testStrain(ellipsoid,t=0TOt=30,dt=.01,dist=1e15,a=1,b=.95,c=1.05,rho0=.8,gaussApproxDensity,omega0=10,arbitrary_precessing_axis_const_rotation_rate)" #Change the last part of the path to the name you want to save the strain tensor file as
#plot_from_file(strain_filepath)
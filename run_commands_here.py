import numpy as np 
import matplotlib.pyplot as plt 
import grav_waves 
import rotations
import celestial_objects
import densities
import angle_functions
import fourierAnalysis


#strainTensor = grav_waves.grav_strain(celestial_objects.ellipsoid_object, 1e16, 0, 30, 0.01, 1, 0.95, 1.05, .8, densities.neutron_star_gaussian_approx, 10, rotations.arbitrary_precessing_axis_const_rotation_rate)
strain_filepath = "/Users/kanlachlan/Documents/VS_Code/Personal Projects/Gravitational_Waves/strain_tensors/testStrain(ellipsoid,t=0TOt=30,dt=.01,dist=1e15,a=1,b=.95,c=1.05,rho0=.8,gaussApproxDensity,omega0=10,arbitrary_precessing_axis_const_rotation_rate)" #Change the last part of the path to the name you want to save the strain tensor file as
strain2_filepath = "/Users/kanlachlan/Documents/VS_Code/Personal Projects/Gravitational_Waves/strain_tensors/InitConds=(celestial_objects.ellipsoid_object,1e20,0,30,0.01,.91,1,.9,.8,densities.neutron_star_gaussian_approx,10,rotations.arbitrary_precessing_axis_const_rotation_rate)"
testStrain_filepath = "/Users/kanlachlan/Documents/VS_Code/Personal Projects/Gravitational_Waves/strain_tensors/testStrain)"

#strainTensors = grav_waves.grav_strain(celestial_objects.ellipsoid_object, 1e20,0, 30, 0.01, .91, 1, .9, .8, densities.neutron_star_gaussian_approx, 10, rotations.arbitrary_precessing_axis_const_rotation_rate )
#grav_waves.strain_writer(strain2_filepath, strainTensors)
#grav_waves.plot_from_file(strain2_filepath)
fourierAnalysis.plotFrequencies(strain2_filepath)


#grav_waves.plot_from_file(testStrain_filepath)
#fourierAnalysis.plotFrequencies(strain_filepath)


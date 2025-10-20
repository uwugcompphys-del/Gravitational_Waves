import numpy as np 
import matplotlib.pyplot as plt
import densities
import rotations
import celestial_objects 
import time 
import grav_waves
import os 
import imageio.v2 as imageio



plt.style.use("dark_background")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12.9


def strain_plotter_animator(source, dist, t0, tmaxGlobal, dt, a, b, c, rho0, density, omega0=0, rotation=rotations.not_rotating, t_axis_limit=10, stride = 10):
    """
    Plot the diagonal gravitational strain terms (representing expansion) and assemble it into a video representation with a sliding time axis
    """
    path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(path, "grav_wave_vidOutput.mp4")
    os.makedirs("grav_wave_frames", exist_ok=True)

    i=0
    tmax_Local = 0 
    tups = grav_waves.grav_strain(source, dist, t0, tmaxGlobal, dt, a, b, c, rho0, density, omega0, rotation)
    frames =[]
    frameNums = []
    print("Constructing Frames...")
    while tmax_Local <= tmaxGlobal: #Make the time widow "slide" across. Let the wave acummuate to time_axis_limit first and then only plot from t=lowerBound to t=time_axis_limit
        times = []
        xExp = []
        yExp =[]
        zExp = []
        if tmax_Local<= t_axis_limit: #"Acummunlation" Phase
            lowerBound = 0
        else: #"Later" Phase
            lowerBound = tmax_Local-t_axis_limit 
        for tup in tups:
            if tup[0]<=tmax_Local and tup[0]>= lowerBound: 
                times.append(tup[0])
                xExp.append(tup[1][0][0]) #Remember tup[1] is the tensor h_ij, need to specify i AND j otherwise it will plot the whole row and result in 3 lines on the same plot
                yExp.append(tup[1][1][1])
                zExp.append(tup[1][2][2])
        
        fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize = (8,12))
        ax1.plot(times, xExp, color="white")
        ax1.set_xlabel("time after first detection (arb.u)")
        ax1.set_ylabel(r"$h_{xx}$, x expansion (1)")

        ax2.plot(times, yExp, color="white")
        ax2.set_xlabel("time after first detection (arb.u)")
        ax2.set_ylabel(r"$h_{yy}$, y expansion (1)")

        ax3.plot(times, zExp, color="white")
        ax3.set_xlabel("time after first detection (arb.u)")
        ax3.set_ylabel(r"$h_{zz}$, z expansion (1)")

        frame_path = f"grav_wave_frames/frame_{i:04d}.png"
        plt.savefig(frame_path)
        plt.close()
        
        frameNums.append(i)
        i+=1 #Increment frame index
        tmax_Local+=dt*stride

    for frameNum in frameNums:
        print(30*"\n", "Frames constructed. Assembling video...")
        print(f"Packing Frame {frameNum} out of {frameNums[-1]}")
        frame_path = f"grav_wave_frames/frame_{frameNum:04d}.png"
        image = imageio.imread(frame_path)
        frames.append(image)

    imageio.mimsave(output_path, frames, fps=30) #set to 30 fps if not simulating anything special
    print("Video saved with path ", output_path)
    print(path)


#strain_plotter_animator(celestial_objects.ellipsoid_object,5e20,0,10,.05, .95, .9, 1, .8, densities.neutron_star_gaussian_approx, 6, rotations.arbitrary_precessing_axis_const_rotation_rate, 2, 1) 
#strain_plotter_animator(celestial_objects.ellipsoid_object,5e20,0,30,.01, .95, .9, 1, .8, densities.neutron_star_gaussian_approx, 10, rotations.arbitrary_precessing_axis_const_rotation_rate, 3,1)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import rotations
import celestial_objects
import densities
import rotations
import celestial_objects 
import time 
import grav_waves

plt.style.use("dark_background")
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12.9


def plotEllipsoid(a:float, b:float, c:float, rotationFunc:callable, omega0:float, tmax:float, dt:float, save:bool=False):
    """
    Return an animation of an ellipsoid described by the equation x^2/a^2 + y^2/b^2 + z^2/c^2 =1 being rotated by rotationFunc over a time from t=0 to t=tmax
    Save the animation if save is True
    """
    print("Generating animation...")
    totalFrames = int(tmax/dt)
 #   print(totalFrames)
    polar = np.linspace(0, np.pi, 1000)
    azimuth = np.linspace(0, 2*np.pi, 1000)

    Polar, Azimuth = np.meshgrid(polar, azimuth)

    x = a*np.cos(Azimuth) * np.sin(Polar)
    y = b*np.sin(Azimuth) * np.sin(Polar)
    z = c*np.cos(Polar)

    border = max(a,b,c)
    ax.set_xlim(-border, border)
    ax.set_ylim(-border, border)
    ax.set_zlim(-border, border)
    showMarkers = True 
    if showMarkers:
            marker = np.array([[0], [b], [0]]) 
            marker2 = np.array([[0], [-b], [0]]) 

    ax.plot_surface(x,y,z, cmap="twilight")
    
    points = np.vstack((x.ravel(), y.ravel(), z.ravel())) #make them into one tensor to prep for applying rotation operator
    def update(frame):
        """
        Update the frame by applying the rotation matrix to the ellipsoid
        """
        ax.clear()
        ax.axis('off')
        ax.view_init(elev = 30, azim=45)
        t = frame*dt
        cur_t = frame*dt #Convert frame to simulation time (frames = cur_t/dt)
        R = rotationFunc(t, omega0)
        ax.set_title(f"Neutron Star with Small Imperfection - Ellipsoidal Approximation, t={cur_t:.2f}")

        newpoints = R @ points
        if showMarkers:
            rotated_marker = R @ marker
            rotated_marker2 = R @ marker2

        rotated_x=newpoints[0].reshape(x.shape) #unpack the bog newpoints tensor back into components
        rotated_y=newpoints[1].reshape(y.shape)
        rotated_z=newpoints[2].reshape(z.shape)  

        ax.plot_surface(rotated_x, rotated_y, rotated_z, cmap="bone", edgecolor="royalblue", linewidth=1/10)
        
        if showMarkers:
            ax.scatter(*rotated_marker, color='blue', s=30)
            ax.scatter(*rotated_marker2, color='blue', s=30)

        ax.set_xlim(-border, border)
        ax.set_ylim(-border, border)
        ax.set_zlim(-border, border)

        return ax

    ani = FuncAnimation(fig, update, frames=totalFrames, interval=100, blit=False)
    print("Animation generated sucessfully. Saving animation...")
    if save:
        ani.save("star_animator_output.mp4")
    print("Animation saved. See output animation for results.")
    plt.show()

#plotEllipsoid(.95, 1, .9, rotations.arbitrary_precessing_axis_const_rotation_rate, 10, 30, .05, True) #omega0 anywhere from 0.01 to 628
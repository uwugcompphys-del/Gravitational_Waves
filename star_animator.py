import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import rotations
import celestial_objects

plt.style.use("dark_background")
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')


def plotEllipsoid(a:float, b:float, c:float, rotationFunc:callable, omega0:float, tmax:float, dt:float):
    """
    Return a plot of an ellipsoid rescribed by the equation x^2/a^2 + y^2/b^2 + z^2/c^2 =1
    """
    totalFrames = int(tmax/dt)
    print(totalFrames)
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

    marker = np.array([[0], [b], [0]]) 

    ax.plot_surface(x,y,z, cmap="twilight")
    
    points = np.vstack((x.ravel(), y.ravel(), z.ravel())) #make them into one tensor to prep for applying rotation operator
    def update(frame):
        """
        Update the frame by applying the rotation matrix to the ellipsoid
        """
        ax.clear()
        ax.axis('off')
        ax.view_init(elev = 45, azim=45)
        t = frame*dt
        cur_t = frame*dt #Convert frame to simulation time (frames = cur_t/dt)
        R = rotationFunc(t, omega0)
        ax.set_title(f"Neutron Star with Small Imperfection - Ellipsoidal Approximation, t={cur_t:.2f} (arb. u)")

        newpoints = R @ points
        rotated_marker = R @ marker

        rotated_x=newpoints[0].reshape(x.shape) #unpack the bog newpoints tensor back into components
        rotated_y=newpoints[1].reshape(y.shape)
        rotated_z=newpoints[2].reshape(z.shape)  

        ax.plot_surface(rotated_x, rotated_y, rotated_z, cmap="bone", edgecolor="royalblue", linewidth=1/10)
        ax.scatter(*rotated_marker, color='blue', s=30)

        ax.set_xlim(-border, border)
        ax.set_ylim(-border, border)
        ax.set_zlim(-border, border)

        return ax

    ani = FuncAnimation(fig, update, frames=totalFrames, interval=1, blit=False)
    plt.show()

plotEllipsoid(.95, 1, .9, rotations.arbitrary_axis_nonConst_rotation_linear_decreasing_rate, 60, 30, .002) #omega0 anywhere from 0.01 to 628
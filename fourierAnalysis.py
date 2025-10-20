import numpy as np 
import matplotlib.pyplot as plt
import csv 
import grav_waves 
import imageio.v2 as imageio

def frequency_domain(filepath):
    """
    Fourier transform all components of the strain tensor stored in filepath into the frequency domain, return the absolute value of the fourier transformed values
    """
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
    dt = times[1]-times[0]
    times = np.array(times) 
    frequencies = np.fft.fftfreq(len(times), d=dt)
    FTh_xx = np.fft.fft(np.array(h_xx))
    FTh_yy = np.fft.fft(np.array(h_yy))
    FTh_zz = np.fft.fft(np.array(h_zz))
    FTh_xy = np.fft.fft(np.array(h_xy))
    FTh_xz = np.fft.fft(np.array(h_xz))
    FTh_yz = np.fft.fft(np.array(h_yz))

    return frequencies, np.abs(FTh_xx), np.abs(FTh_yy), np.abs(FTh_zz),np.abs( FTh_xy), np.abs(FTh_xz),np.abs(FTh_yz)

def plotFrequencies(filepath):
    """
    Plot the frequencies of the data in the file with path filepath
    """
    frequencies, FTh_xx, FTh_yy, FTh_zz, FTh_xy,FTh_xz, FTh_yz = frequency_domain(filepath)
    plt.style.use('default') 

    f, axs = plt.subplots(3,2,figsize=((12,10)))
    axs=axs.flatten()
    f.suptitle("Fourier Transform of the Gravitational Wave Strain Tensor Components")

    axs[0].plot(frequencies,FTh_xx, color = "black")
    axs[0].set_xlabel("frequency (arb. u)")
    axs[0].set_ylabel("amplitude (arb.  u)")

    axs[2].plot(frequencies,FTh_yy, color = "black")
    axs[2].set_xlabel("frequency (arb. u)")
    axs[2].set_ylabel("amplitude (arb. u)")
    
    axs[4].plot(frequencies,FTh_zz, color = "black")
    axs[4].set_xlabel("frequency (arb. u)")
    axs[4].set_ylabel("amplitude (arb. u)")

    axs[1].plot(frequencies,FTh_xy, color = "black")
    axs[1].set_xlabel("frequency (arb. u)")
    axs[1].set_ylabel("amplitude (arb. u)")

    axs[3].plot(frequencies,FTh_xz, color = "black")
    axs[3].set_xlabel("frequency (arb. u)")
    axs[3].set_ylabel("amplitude (arb. u)")

    axs[5].plot(frequencies,FTh_yz, color = "black")
    axs[5].set_xlabel("frequency(arb. u)")
    axs[5].set_ylabel("amplitude (arb. u)")

    print("Plotting complete. See output plot for results.")

    plt.tight_layout()
    plt.show()    
    

#plotFrequencies("/Users/kanlachlan/Documents/VS_Code/Personal Projects/Gravitational_Waves/strain_tensors/testStrain")
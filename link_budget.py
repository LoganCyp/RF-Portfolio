'''
 The purpose of this script is to calculate the received power given frequency, the transmit power, 
 and the transmit & receive gains, as well as a linearly spaced array of distances to calculate over

 The received power is plotted over distance given the following constant parameters
 
 GTx = 20dB
 GRx = 0dB
 PTx = 1mW

 We are given three cases to plot, when f = 900 MHz, 1.5 GHz and 17.7 GHz.

 It is also required to calculate the effective aperature of the Tx and Rx antennas for each case.

 We are given a range of 10km to 38,000 km
'''

# Import necessary libraries for array manipulation and plotting
import numpy as np
import matplotlib.pyplot as plt

# Calculate the link budget, only require the frequency to be entered, and allow for GTx, GRx, PTx, and R to be changed but default to our parameters
# Note that GTx_dB and GRx_dB must be in dB for proper functionality
def link_budget(frequency, GTx_dB = 20, GRx_dB = 0, PTx = 1e-3, R = np.linspace(1e4, 3.8e7, 1000)):
    # Speed of light constant for calculating wave length
    c = 3e8

    # Convert GRx and GTx from decibals to a linear scale
    GRx_lin = 10 ** (GRx_dB / 10)
    GTx_lin = 10 ** (GTx_dB / 10)

    # Calculate the wavelength by dividing the speed of light over the frequency
    wavelength = c / frequency

    # Calculate the free-space loss
    fs_loss = (wavelength / (4 * np.pi * R))**2

    # Calculate the power received linearly
    PRx = PTx * GTx_lin * GRx_lin * fs_loss

    # Convert to dB
    PRx = 10 * np.log10(PRx)

    # Return PRx and R for plotting, GTx_dB and GRx_dB for effective aperature calculation
    return PRx, GTx_dB, GRx_dB, R, wavelength

# Calculate the effective aperature for Tx and Rx gain
def effective_aperature(g_dB, wavelength):

    # Convert the gain to a linear scale
    g_lin = 10**(g_dB / 10)

    # Calculate the effective aperature
    A_eff = (g_lin * wavelength**2) / (4 * np.pi)
    return A_eff

# Create an array that holds the required frequencies and the corresponding labels
frequencies = [900e6, 1.5e9, 17.7e9]
labels = ['900 MHz', '1.5 GHz', '17.7 GHz']

# Loop through all frequencies and keep track of index for each label
for idx, frequency in enumerate(frequencies):
    # Calculate the received power
    PRx, GTx_dB, GRx_dB, R, wavelength = link_budget(frequency)
    # Calculate the effectieve aperature for the Tx and Rx gains
    A_Tx = effective_aperature(GTx_dB, wavelength)
    A_Rx = effective_aperature(GRx_dB, wavelength)
    # Plot the distance (km) vs power received (dBW)
    plt.plot(R / 1e3, PRx)
    # Display a title that shows the effective aperatures and frequency
    plt.title(f'Received Power vs Distance @ {labels[idx]} \n Effective Aperature of Tx Antenna: {A_Tx:.2e} m² \n Effective Aperature of Rx Antenna: {A_Rx:.2e} m²')
    # Label the axes
    plt.xlabel('Distance (km)')
    plt.ylabel('Received Power (dBW)')
    # Enabe a grid for the graph
    plt.grid(True)
    plt.show()

 
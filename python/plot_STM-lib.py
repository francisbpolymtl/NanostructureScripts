import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy import ndimage
import sys

# Load data from the specified file
x, y, z = np.loadtxt(sys.argv[1], unpack=True)

# Apply correction for the mirror effect by flipping the y-values
y = -y

# Define the grid for the 2D plot
xi = np.unique(x)
yi = np.unique(y)
X, Y = np.meshgrid(xi, yi)

# Interpolate the z-values onto the grid
points = np.column_stack((x, y))
grid_z = griddata(points, z, (X, Y), method='linear')

# Apply Gaussian filter for smoothing by default (optional and not enabled by default)
im_Z = ndimage.gaussian_filter(grid_z, sigma=5, mode='nearest') 

# Create the 2D plot with a color map
plt.figure(figsize=(8, 6))
im = plt.imshow(grid_z, cmap='jet', extent=(xi.min(), xi.max(), yi.min(), yi.max())) # Replace grid_z with im_Z to enable gaussian filter

# Add a color bar
colorbar = plt.colorbar(im, orientation='vertical', label='Current (A)')

# Remove x and y axis labels
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

# Save the plot with a white border
label = sys.argv[1].replace(".dat","")
plt.savefig(f'{label}.png', bbox_inches='tight', pad_inches=0.1)


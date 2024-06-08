import matplotlib.pyplot as plt
import numpy as np

# Enable interactive mode
plt.ion()

# Create a figure and an axis
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-')

# Initialize the plot
def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)
    return ln,

# Function to update the plot
def update(value):
    xdata.append(value)
    ydata.append(np.sin(value))  # Example: y = sin(x)
    ln.set_data(xdata, ydata)
    plt.draw()
    plt.pause(0.001)

# Initialize the plot
init()

# Example usage: calling update to update the plot in real-time
for val in np.linspace(0, 10, 1000):
    update(val)

plt.ioff()
plt.show()

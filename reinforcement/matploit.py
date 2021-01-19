import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    t = np.array([2, 2, 8, 5, 7, 6, 1, 4])  # sample points
    s = np.array([10, 5, 4, 8, 5, 4, 2, 9])
    scatter = plt.scatter(t, s)  # create a fig and a plot ax.plot(t, s) # x-axis and y-axis
    plt.grid()
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.show()

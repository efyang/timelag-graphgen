import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = np.random.rand(100)
ys = np.random.rand(100)
zs = np.random.rand(100)
ax.scatter(xs, ys, zs)

fig.show()

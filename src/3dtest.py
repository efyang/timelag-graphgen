from matplotlib.tri import Triangulation
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
X = []
for i in range(8):
    t = np.linspace(0,2*np.pi,np.random.randint(30,50))
    for j in range(t.shape[0]):
        # random circular objects...
        X.append([
            (-0.05*(i-3.5)**2+1)*np.cos(t[j])+0.1*np.random.rand()-0.05,
            (-0.05*(i-3.5)**2+1)*np.sin(t[j])+0.1*np.random.rand()-0.05,
            i
        ])

X = np.array(X)# compute the convex hull of the points
cvx = ConvexHull(X)

x, y, z = X.T

# cvx.simplices contains an (nfacets, 3) array specifying the indices of
# the vertices for each simplical facet
tri = Triangulation(x, y, triangles=cvx.simplices)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.hold(True)
ax.plot_trisurf(tri, z)
# ax.plot_wireframe(x, y, z, color='r')
ax.scatter(x, y, z, color='r')

plt.show()

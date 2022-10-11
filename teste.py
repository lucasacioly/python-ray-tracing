import numpy as np

from components.basic_geom import Vector3

a = np.array([1, 2, 3])

b = np.array([3, 3, 3])

c = Vector3(*(a - b))
c.normalize()

print(c.vector)
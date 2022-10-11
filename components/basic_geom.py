from msilib.schema import Class
from turtle import onclick
import numpy as np 

class Vector3:
    vector = None

    def __init__(self, x, y, z):
        self.vector = np.array([x, y, z])
    
    def normalize(self):
        self.vector = self.vector/np.linalg.norm(self.vector)

class Point(Vector3):
    pass

class Color(Vector3):
    
    def __init__(self, x, y, z):
        self.vector = np.array([float(x)/255, float(y)/255, float(z)/255])
import numpy as np
import matplotlib.pyplot as plt

class Field:
    def __init__(self,map_file,size_pixel=50):
        self.width,self.height,self.map=self.map_data(map_file,size_pixel)
        self.size_pixel=size_pixel
    
    def map_data(self,map_file,size_pixel):
        im = plt.imread(map_file)
        return im.shape[1],im.shape[0],np.zeros((im.shape[1]//size_pixel,im.shape[0]//size_pixel))

class FieldHexagon(Field):
    def map_data(self,map_file,size_pixel):
        im = plt.imread(map_file)
        n=int(np.round(im.shape[1]/(np.sqrt(3)*size_pixel)-1/2))
        m=int(np.round(im.shape[0]*2/(3*size_pixel)-1/3))
        width=np.sqrt(3)*size_pixel*(n+1/2)
        height=size_pixel*(3/2*m+1/2)
        return width,height,np.zeros((n,m))

class FieldTriangle(Field):
    def map_data(self,map_file,size_pixel):
        im = plt.imread(map_file)
        n=int(np.round(im.shape[1]/(np.sqrt(3)*size_pixel/2)))
        m=int(np.round(im.shape[0]/(size_pixel/2)-1))
        width=n*np.sqrt(3)*size_pixel/2
        height=size_pixel*(m+1)/2
        return width,height,np.zeros((n,m))
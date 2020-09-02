import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

from scipy.spatial.transform import Rotation as R

import analysis.calcAccuracy as calcAna
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def drawVector(originVec,directionVec,color="k"):
    #returns a Arrow3D object starting at originVec and going in the directionVec direction
    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', shrinkA=0, shrinkB=0)
    p0=originVec
    p1=originVec+directionVec
    a = Arrow3D([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], **arrow_prop_dict, color=color)
    return a

def getOriginAndDirectionFromHomMatrix(homMatrix):
    r=homMatrix[0:3,0:3]
    p=-homMatrix[0:3,3]
    baseX=np.array([1,0,0]).reshape([3,1])
    baseY=np.array([0,1,0]).reshape([3,1])
    baseZ=np.array([0,0,1]).reshape([3,1])
    # print(baseX)
    vX=r@baseX
    vY=r@baseY
    vZ=r@baseZ
    return [p,vX,vY,vZ]

def createArtists(plot,listOfHomMatrices):
    #added coordinate system 
    #x:cyan, y:magenta, z:yellow
    listArtists=[]
    for homMatrix in listMeasHomMatrix:
        # print(homMatrix)
        p,vX,vY,vZ=getOriginAndDirectionFromHomMatrix(homMatrix)
        x=drawVector(p,vX,color="c")
        y=drawVector(p,vY,color="m")
        z=drawVector(p,vZ,color="y")
        plot.add_artist(x)
        plot.add_artist(y)
        plot.add_artist(z)
    return listArtists
def createArtists2(plot,listOfHomMatrices):
    #added coordinate system 
    #x:cyan, y:magenta, z:yellow
    listArtists=[]
    for homMatrix in listMeasHomMatrix:
        p,vX,vY,vZ=getOriginAndDirectionFromHomMatrix(homMatrix)
        x=drawVector(p,vX,color="r")
        y=drawVector(p,vY,color="g")
        z=drawVector(p,vZ,color="b")
        plot.add_artist(x)
        plot.add_artist(y)
        plot.add_artist(z)
    return listArtists
if __name__ == '__main__':
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_xlabel('X')
    ax1.set_xlim(-10, 10)
    ax1.set_ylabel('Y')
    ax1.set_ylim(-10, 10)
    ax1.set_zlabel('Z')
    ax1.set_zlim(-10, 10)

    #base CoordinateSystem
    x=drawVector(np.array([0,0,0]),np.array([1,0,0]),color="r")
    y=drawVector(np.array([0,0,0]),np.array([0,1,0]),color="g")
    z=drawVector(np.array([0,0,0]),np.array([0,0,1]),color="b")
    ax1.add_artist(x)
    ax1.add_artist(y)
    ax1.add_artist(z)
    # Give them a name:
    ax1.text(0.0, 0.0, -0.1, r'$0$')
    ax1.text(1.1, 0, 0, r'$x$')
    ax1.text(0, 1.1, 0, r'$y$')##

    ######ACTUAL DATA#####

    experimentNumber="1"
    date="20200827"

    regHomMatrix,listMeasHomMatrix,laserHomMatrix=calcAna.getMatrices(experimentNumber,date)
    listOfVive=[]
    for num in range(0,len(listMeasHomMatrix)):  
        vive2=regHomMatrix@calcAna.invertHomMatrix(listMeasHomMatrix[num])
        listOfVive.append(vive2)
    # createArtists(ax1,laserHomMatrix.extend(listOfVive))
    # print(listOfVive[0])
    createArtists(ax1,listOfVive)
    plt.show()
import matplotlib.pyplot
import kwant
lat = kwant.lattice.square()
sys = kwant.Builder()
def disk(pos):
    x, y = pos
    return x**2 + y**2<13**2
sys[lat.shape(disk, (0, 0))] = 0.5
sys[lat.neighbors(2)] = 1
kwant.plot(sys)


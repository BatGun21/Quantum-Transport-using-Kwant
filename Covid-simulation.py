# Inspired by and a modified version of
# https://www.hackster.io/pepis/animated-sir-model-for-coronavirus-spread-72c700
# Modified by: svs@cse

import math
import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle


# Points on the grid are of type People
class People:
    def __init__(self, src, dst, i):
        self.srcx, self.srcy = src
        self.dstx, self.dsty = dst
        self.iden = i

        #current status. Note that I am also trying
        # to illustrate encapsulation concept here
        self.__infected = False
        self.__healthy = True
        self.__quarantined = False
        self.__recovered = False
        
        #speed
        self.speed = (np.random.random()+0.5)*100
        
        #time at which infection happened
        self.infectionTime = -1
        
        # time for recovering from the infection
        self.recoveryTime = np.random.random()*100

        self.set_displacement()
        
        self.firstInfection = False
        self.secondInfection = False
        
    def isInfected(self):
        return self.__infected
    
    
    def isHealthy(self):
        return self.__healthy
    
    def set_quarantined(self):
        self.__quarantined = True
        
    # in order to animate the movement of people
    # set the displacement per unit of time
    def set_displacement(self): 
        if self.__quarantined:
            self.deltax = 0
            self.deltay = 0
        else:
            self.deltax = (self.dstx - self.srcx) / self.speed
            self.deltay = (self.dsty - self.srcy) / self.speed

    def get_color(self):
        if self.__infected:
            return 'red'
        if self.__healthy:
            return 'green'
        if self.__quarantined:
            return 'gray'
        
    # set the time of infection
    def set_infection(self, t):
        if not self.firstInfection:
            self.firstInfection = True
        else:
            if not self.secondInfection:
                self.secondInfection = True
                
        self.__infected = True
        self.__healthy = False
        self.infectionTime = t
        
    def hasBeenInfectedTwice (self):
        return self.secondInfection
    
    # check if a person is infected and spent sufficient time in recovery
    def check_and_set_recovered(self, t): 
        if self.__infected and ((t - self.infectionTime) >= self.recoveryTime):
            self.__infected = False
            self.__healthy = True
            self.__recovered = True
            if self.__quarantined:
                self.__quarantined = False
            return True
        else: return False

    def hasRecovered(self):
        return self.__recovered
        
    # change destination once reached destx
    def changeDst(self, x, y):
        # check if p has reached or crossed dst then reset the dst
        self.dstx = x
        self.dsty = y
            
    # this function helps to move the person towards destx, desty by delta
    def moveSrc(self):
        if (not self.__quarantined): 
            self.srcx = self.srcx + self.deltax
            self.srcy = self.srcy + self.deltay

        # if the dest is reached, then change the dest.
        if  abs(self.srcx - self.dstx)<3 and abs(self.srcy-self.dsty)<3:
            self.changeDst(np.random.random()*100, np.random.random()*100)
            self.set_displacement()

    def getDist(self,x,y):
        return math.sqrt((self.srcx-x)**2+(self.srcy-y)**2)

###########################################
# 1.  creating People points
# 2.  Infect a fraction of the population
###########################################

NumP = 350
people = []
infected_population = 0.05 # to begin with 5% population is infected 
quarantined_population = 0.4 # probability of quarantining -- that is getting detected  
num_infected = 0
radiusOfInfection = 4 # in terms of pixels 
probabiliyOfTransmission = 0.4 # 40% probability of transmission

for i in range(NumP):
    p  = People((np.random.random()*100, np.random.random()*100),
                (np.random.random()*100, np.random.random()*100),
                i)

    if np.random.random()< infected_population:
        p.set_infection(0)
        num_infected = num_infected + 1
        # note that not every infected is quarantined
        if np.random.random()< quarantined_population:
            p.set_quarantined()
    
    people.append(p)

###############################
# code for creating the plots 
###############################

fig = plt.figure(figsize=(16,8), dpi=80)
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

# set the axis for the two plots
ax1.axis('off')
ax2.axis([0, 1000, 0,  NumP])

# adding a enclosing rectangle to the scatter palot
ax1.add_patch(Rectangle((0,0),100,100,fill=False))

# Name the axes
ax2.set_xlabel("Time")
ax2.set_ylabel("Number of People")

# Add two curves on the second plot
inf,=ax2.plot(num_infected,color="red",label="Infection")
rec,=ax2.plot(num_infected,color="green",label="Recovery")

# Add a legend
ax2.legend()

scatPlt= ax1.scatter([p.srcx for p in people],
                     [p.srcy for p in people], c = 'green',s=8)

recPlotData=[0]
infPlotData=[num_infected]
time=[0]

# code for animating the next frame
def animationUpdate(i,recPlotData, infPlotData, time):
    infectedCnt  = 0
    recoveredCnt = 0
    colors = []

    for p in people:
        #check if p can be recovered at time step i
        p.check_and_set_recovered(i)
        # move the person if not quarantined
        p.moveSrc()
        # if p is infected, increment the infected count
        # and check if others in the neighborhood can be infected
        if p.hasRecovered():
            recoveredCnt +=  1
        if p.isInfected():
            infectedCnt = infectedCnt + 1
            for p1 in people:
                if p1.isInfected() or p1.iden == p.iden:
                    pass
                else: 
                    if p.getDist(p1.srcx, p1.srcy) <= radiusOfInfection and not p1.hasBeenInfectedTwice():
                        if np.random.random() <= probabiliyOfTransmission:
                            p1.set_infection(i)
                            if np.random.random() <= quarantined_population:
                                p1.set_quarantined()
                            
        colors.append(p.get_color())

    #fill in the newly generated data
    recPlotData.append(recoveredCnt)
    infPlotData.append(infectedCnt)
    time.append(i)

    # setup the plots for the generated data per frame
    newOffsets=np.array([[p.srcx for p in people],
                         [p.srcy for p in people]])
    scatPlt.set_offsets(np.ndarray.transpose(newOffsets))
    scatPlt.set_color(colors)

    inf.set_data(time, infPlotData)
    rec.set_data(time, recPlotData)
    
    return inf,rec,scatPlt

#invoke the library function to animate the new frames at specified time intervals
anim = FuncAnimation(fig, animationUpdate, interval=25, fargs=(recPlotData, infPlotData, time), blit=True)

#plt.isinteractive()
plt.show()
#plt.savefig('scat.png')



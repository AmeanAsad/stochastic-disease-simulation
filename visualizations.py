#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 07:18:57 2020

@author: ameanasad
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PandemicModel import PandemicSpread, Node



"""
These parameters control the whole experiment. Modify them to get different
results. 
"""
###################
size = 300
nodes = 160
infectionRate = 0.5
radius = 7
speed = 1.9
####################


box = PandemicSpread(size, nodes, infectionRate, radius, speed)
box.startInfection()
box.deployNodes()

fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                      xlim=(-size*2,size*2), ylim=(-size, size)) 
 
particles, = ax.plot([], [], color="#26689e",  ms=6, marker="o",linestyle="None")
infected, = ax.plot([], [], color="#db5e5c",  ms=6, marker="o",linestyle="None")
dead, = ax.plot([], [], color="#615e5e",  ms=6, marker="o",linestyle="None")
recovered, = ax.plot([], [],color="#7acf95",  ms=6, marker="o",linestyle="None")
rect = plt.Rectangle([-size*2,-size],
                      size*4,
                      size*2,
                      ec='none', lw=2, fc='none')    
ax.add_patch(rect)



def init():
    """initialize animation"""
    global box, rect
    particles.set_data([], [])
    infected.set_data([], [])
    dead.set_data([], [])
    recovered.set_data([], [])
    rect.set_edgecolor('none')
    return  infected, particles, dead,recovered, rect


def animate(i):
    """perform animation step"""
    global box, rect, ax, fig
    box.updateNodes()
    
    #Not the best variable assignment but it works 
    X,Y = box.getSample("Susceptible")
    M,N = box.getSample("Infected")
    Z,V = box.getSample("Dead")
    H,G = box.getSample("Recovered")
    
    rect.set_edgecolor('k')
    particles.set_data(X, Y)
    particles.set_markersize(6)
    infected.set_data(M, N)
    infected.set_markersize(6)
    dead.set_data(Z, V)
    dead.set_markersize(6)
    recovered.set_data(H, G)
    recovered.set_markersize(6)
    return infected, particles, dead, recovered, rect


def visualizeParticles():
    """
    Change interval to change the frame rate of the simulation.
    Larger interval means slower frame rate and vice versa. 
    The interval also impacts the actual speed of the particles, 
    which has an impact on the experiment. So keep it constant when running 
    multiple experiments to compare response to various parameter changes.

    Returns
    -------
    ani : Animation figure

    """
    ani = animation.FuncAnimation(fig, animate, frames=5000,
                              interval=10, blit=True, init_func=init)
    return ani



def SirModelPlot():
    
    
    fig2 = plt.figure(figsize=(6,4))
    plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
    ax2 = plt.axes()
    
    im = ax2.stackplot([],[], labels=[ 'infected','vulnerable','removed'],
                  colors=['#db5e5c','#26689e','#7acf95'])    
    Dead  = {'X': [], "Y": []}
    Recovered  = {'X': [], "Y": []}
    Infected  = {'X': [], "Y": []}
    Susceptible  = {'X': [], "Y": []}    
    n = 0
    loop = True
    
    while loop:
        if box.getInfectionNo() == 0:
            break
        n+=1
        x = list(range(0,n))
        box.updateNodes()
        Infected['X'].append(box.getInfectionNo())
        Dead['X'].append(box.getDeathsnNo())
        Recovered['X'].append(box.getRecoveredNo())
        Susceptible['X'].append(box.getSusceptibleNo())
       
    y = [Infected['X'],Susceptible['X'],Recovered["X"], Dead["X"] ]
    #each artist object is a stackplot figure
    im = ax2.stackplot(x,y, labels=[ 'infected','vulnerable','removed'],
              colors=['#db5e5c','#26689e','#7acf95', '#615e5e'])
    
    plt.show()
    return None


"""
Uncomment the following line to show the SIR Plot when running
"""
# SirModelPlot()


"""
Uncomment the following line to show the particle animation when running
"""
# visualizeParticles()




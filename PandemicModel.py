#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 19:08:07 2020

@author: ameanasad
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.neighbors import KDTree
import random as r
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'

# Random Seed set to 0 initializes the same pseudorandom number generator for multiple experiments.
# Comment the random seeds out to use a different random generator everytime you run the code
r.seed(0)
np.random.seed(0)

class PandemicSpread(object):
    
    def __init__(self, size, nodes, infectionRate, radius, speed):
        #nodes is the number of particle in the experiment
        self.nodeSize = nodes
        # Size is the dimension of the enclosing container for the particles
        self.size = size
        self.nodes_all = {"Infected": [],
                      "Susceptible": [],
                      "Dead": [],
                      "Recovered" : []}
        self.infectionRate = infectionRate
        self.radius = radius
        self.speed = speed
        
    def deployNodes(self):
        """
        Deploy all the nodes in random positions
        """
        for i in range(self.nodeSize):
            newNode = Node(self.size, "Susceptible", self.speed)
            self.nodes_all['Susceptible'].append(newNode)   
                  
    def startInfection(self):
        """
        Start infection by deploying one random infected node. 
        """
        newNode = Node(self.size, "Infected", self.speed )
        self.nodes_all['Infected'].append(newNode)
        
    def checkInfection(self, node):
        """
        

        Parameters
        ----------
        node : Object
            A susceptible type node object.

        Returns
        -------
        Boolean
            True if node becomes infected, false otherwise.

        """
        
        # Used a K-dimensional tree to find neighbors within a givin radius
        infected = self.getInfectedCoordinates()
        infected = np.array(infected)
        node = np.array([node.getCoordinates()])
        tree = KDTree(infected, leaf_size = 20)
        # We query the neighbors based on the radius of infection
        indices = tree.query_radius(node, r=self.radius)
        
        if(len(indices[0]) > 0):
             # Added another layer of infection checking by using the infection rate
             state = np.random.choice( 
                    [False, True], 
                    1,
                    p=[1-self.infectionRate, self.infectionRate]
                    )
             return state[0]
        else:
            return False
  
    def updateNodes(self):
        """
        Updates all node position and updates new infections, recoveries and deaths.
        """
        infections = []
        recoveries = []
        deaths = []
        
        for node in self.nodes_all["Susceptible"]:
            node.takeStep()
            if node.state == "Susceptible": 
                infected = self.checkInfection(node)
                if infected==True:
                    infections.append(node)
    
        for node  in self.nodes_all['Infected']:
            node.takeStep() 
            if node.state == "Recovered":
                recoveries.append(node)  
            if node.state == "Dead":
                deaths.append(node)
        
        for node in self.nodes_all['Recovered']:
            node.takeStep()
              
        for infection in infections:
            infection.changeState("Infected")
            self.nodes_all["Susceptible"].remove(infection)
            self.nodes_all["Infected"].append(infection)
            
        for recovery in recoveries: 
             self.nodes_all["Infected"].remove(recovery)
             self.nodes_all["Recovered"].append(recovery)
             
        for death in deaths: 
             self.nodes_all["Infected"].remove(death)
             self.nodes_all["Dead"].append(death)

    def getInfectedCoordinates(self):
        """
        Gets the coordinates of all infected nodes. Coordinates are represented
        in a tuple.

        Returns
        -------
        nodes : list
            List of 2-tuple coordinate vectors.

        """
        nodes = self.nodes_all['Infected']
        nodes = map(lambda node: node.getCoordinates(), nodes)
        nodes = list(nodes)
        return nodes 
    
    def getCoordinates(self, name):
        """
        Gets the coordinates of nodes. Coordinates are represented
        in a tuple.

        Returns
        -------
        nodes : list
            List of 2-tuple coordinate vectors.

        """
        nodes = self.nodes_all[name]
        nodes = map(lambda node: node.getCoordinates(), nodes)
        nodes = list(nodes)
        return nodes 
    
    def getSample(self, name):
        """
        Parameters
        ----------
        name : String
            State of nodes desired.

        Returns
        -------
        Two lists of node coordinates.
        """
        nodes = self.nodes_all[name]
        nodes = map(lambda node: node.getCoordinates(), nodes)
        nodes = list(nodes)
        
        X = map(lambda node: node[0], nodes)
        Y = map(lambda node: node[1], nodes)
        
        X = list(X)
        Y = list(Y)
        return X,Y
    
    def getApiResponse(self):
        """
        I wrote this function so the coordinates, and colors of the nodes can 
        be exported as an API response to be used in different visualization
        frameworks. 

        Returns
        -------
        nodes : list of dictionaries
            Each dict object contains the coordinates and color of the node.

        """
        states = ["Infected", "Susceptible", "Recovered", "Dead"]
        nodes =[]
        for state in states:
            nodes += self.nodes_all[state]      
        func = lambda node: {"Coord": node.getCoordinates(), "Color": node.getColor()}
        
        nodes = map(func, nodes)
        nodes = list(nodes)
        return nodes
    
    def getInfectionNo(self):
        return len(self.nodes_all['Infected'])
    
    def getSusceptibleNo(self):
      return len(self.nodes_all['Susceptible'])
  
    def getRecoveredNo(self):
      return len(self.nodes_all['Recovered'])
  
    def getDeathsnNo(self):
      return len(self.nodes_all['Dead'])

    
    
class Node(object):
    def __init__(self, max_coordinate, state, speed):
        self.x = r.randint(-max_coordinate*2,max_coordinate*2)
        self.y = r.randint(-max_coordinate,max_coordinate)       
        self.state = state
        self.colorMap = {
            "Susceptible": "blue",
            "Infected": "red",
            "Recovered": "Green",
            "Dead": "black"}
        self.counter = 0
        self.angle = np.random.uniform(0,2*np.pi)
        self.max = max_coordinate
        self.speed = speed
        
    def getCoordinates(self):
        return [self.x,self.y] 
    
    def takeStep(self):
        if self.state == "Infected":
            if self.counter == 400:
                
                state = np.random.choice( 
                    ['Dead', 'Recovered'], 
                    1,
                    p=[0.1, 0.9]
                    )
                self.state = state[0]
            else:
                self.counter+=1
        
        x = self.x
        y = self.y
        y += np.cos(self.angle)*self.speed
        x += np.sin(self.angle)*self.speed
        if abs(x) < self.max*2:
            self.x = x
        else:
            self.angle = np.random.uniform(0,2*np.pi)
        if abs(y) < self.max - 5:
            self.y = y
        else:
            self.angle = np.random.uniform(0,2*np.pi)
            
    def state(self):
        return self.state
    def getColor(self):
        return self.colorMap[self.state]
    def changeState(self, state):
        self.state = state
        
    def __str__(self):
        return str((self.x,self.y))
    
    def __repr__(self):
        return str((self.x,self.y))
    




"""
Below is a sample test run to show how the model is used. 
"""


# size = 300
# nodes = 160
# infectionRate = 0.5
# radius = 7
# speed = 1.9
# steps = 50
# pandemic = PandemicSpread(size, nodes, infectionRate, radius, speed)
# pandemic.startInfection()
# pandemic.deployNodes()

# for step in range(steps):
#     pandemic.takeStep()







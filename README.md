# pandemic-simulations
A simulation model for pandemic spread using population dynamics of infectious diseases


# Installation
To download repo you can:
 - Use git clone:
  <pre> <code> https://github.com/AmeanAsad/pandemic-simulations.git </code> </pre>
 - Download zip file from Git. 
 
 After download, you need to install required packages:
  - Open terminal
  - cd to the root directory of the repo. 
  - Run <code> pip install -r requirements.txt </code> 
 
 
#Usage

Here is a sample to run the Pandemic Model:
 <pre> <code> 
     size = 300
     nodes = 160
     infectionRate = 0.5
     radius = 7
     speed = 1.9
     steps = 50
     pandemic = PandemicSpread(size, nodes, infectionRate, radius, speed)
     pandemic.startInfection()
     pandemic.deployNodes()

     for step in range(steps):
         pandemic.takeStep()
  </code> </pre>
 
To run the Visualizations, open the <code> visualizations.py </code> folder and:
 - Run <code> SirModelPlot() </code> to visualize the SIR stack plot.
 - Run <code> visualizeParticles() </code>  to visualize the particle simulation.
 

 


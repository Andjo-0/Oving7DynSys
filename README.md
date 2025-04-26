# What is this?
This is a Cosimulation of a Cart, Inverted Pendulum and regulator system with the goal of using the cart to stabilise the angle of the inverted pendulum. 

# How to use

First you have to run the Build.Py file in order to create the 3 FMUS.
Once this is done running the Simulation.py file will run the simulation between the 3 FMUS. In this file you can
change the regulator parameters to tune the system, as well as change the values of the system. 

#### NB: No euler integration is used for the position and velocity of the cart as it made the system too unstable. 

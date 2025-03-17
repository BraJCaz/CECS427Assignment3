# CECS427Assignment3
# Brandon Cazares
# Professor Ponce 
# CECS 427 Sec 1 
# Due Date 3/24/2025

# Purpose 
- In this assignment, we're going to write a python program that has game theory because we need to calculate both nash equilibirum and social optimality in a directed network.

# Requirement
- This assignment requires us to create a python assingment that runs in a terminal. This program accepts a directed graph where each edge has parameters a and b of the polynomial factor ( a x + b).
- This program also must print the number of vehicles in each edge obtained from the travel equilibrium and the social optimality.
- We need to use this command to execute this Python script.
python ./traffic_analysis.py digraph_file.gml  n initial final -- plot.

# Description of Parameters 
- This is the command to execute the Python script traffic_anaylsis.py located in the current directory, read the file digraph_file.gml and the number of vehicles in the network as well as the initial and final node. 
- Here, digraph will be used for the analysis and the format is Graph Modeling Language (GML) which describes the digraph's structure with attributes.
- This program should read attributes of the nodes and edges in the file and print out the number of drivers in each edge at btoh the nash equilibrium and social optimal.

--plot
# Finally, we plot the directed graph and the polynomials of every edge. 
Examples:
python ./traffic_analysis.py traffic.gml 4 0 3 --plot

- When I ran this example on my machine, it gave me 4 vehicles, 0 as my start position and 3 as my end position. 

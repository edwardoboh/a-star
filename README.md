# Introduction
A* is a pathfinding algorithm that finds the shortest route between two points by intelligently combining actual cost traveled (g-score) with estimated remaining cost (h-score).* Instead of blindly exploring all directions like simpler algorithms, A* uses the evaluation function f(n) = g(n) + h(n) to always examine the most promising path next.

# About the Project
This project is a simple A* algorithm visualizer, built with python and the pygame
library. It finds the shortest path between two points initially inputed by the user, 
together with obstacles between the points defined.

## Test Program
To test this code on your pc, simply clone the repository and run the a_start.py file.
Ensure that you are running a version of python 3 and not 2.7.

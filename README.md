# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Because we first find a pair of boxes in the same unit who have the same exact pair of possibilities. Then we choose one value for each one of those boxes which minimizes
the legal values for all other boxes in that unit as now we have assigned values to each of these boxes and will now perform search() down both of these possible branches 
and see which one will return a valid result. And now since we can take out both of these possible values in the naked twins from other boxes in any of the units this pair
resides in, we possibly might be assigning definite values to other boxes which will then further eliminate more possibilities from other boxes - thus propagating the constraint
of the naked twins to a possible solution

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Same as we use constraint propagation to solve a 'normal' sudoku. All we have done is added 2 more units. So when we have a constraint (like a naked twin in a unit, an assigned value in 
one box etc..) then we can eliminate that value from being a possible value for all peers of that box. This reduces the number of possiblities in every peer constraint which in turn could 
result in a peer having a definite value in which then we could eliminate that value from the peers of that peer and so on. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
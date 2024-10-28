# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    fringe = util.Stack()

    start_state = problem.getStartState()  # we need the first state and an empty path

    fringe.push((start_state, [])) # state , path 

    visited = set() # a set to store the visited states

    while not fringe.isEmpty():
        state, path = fringe.pop() # tuple

        if problem.isGoalState(state):
            return path
        
        if state not in visited:
            visited.add(state)

            # that's were the magic is happening
        for successor, action, stepCost in problem.getSuccessors(state):  # stepCost doesn't do anything but is essentiall, but is needed for the getSuccessors fun
            if successor not in visited:
                new_path = path + [action] 
                fringe.push((successor, new_path))

    return[]

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Create a queue for states to explore (FIFO).
    fringe = util.Queue()
            
    # Get the initial state of the problem and add it to the queue with an empty path.
    start_state = problem.getStartState()
    fringe.push((start_state, []))  # state, path

    # Create a set to store visited states.
    visited = set()

    # Continue searching while there are states in the queue.
    while not fringe.isEmpty():
        # Pop the next state from the queue and its corresponding path.
        state, path = fringe.pop()

        # Check if the current state is a goal. If so, return the path.
        if problem.isGoalState(state):
            return path

        # If the state has not been visited yet, add it to the set of visited states.
        if state not in visited:
            visited.add(state)

            # Explore the successors of the current state.
            for successor, action, _ in problem.getSuccessors(state):
                # Check if the successor has not been visited already.
                if successor not in visited:
                    # Create the new path by adding the current action to the existing path.
                    new_path = path + [action]
                    
                    # Add the successor and the updated path to the queue for further exploration.
                    fringe.push((successor, new_path))

    # If no solution is found, return an empty list.
    # This could occur if the problem has no goal state or is not fully connected.
    return []


    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    
    start_state = problem.getStartState()  # we need the first state and an empty path

    fringe.push((start_state, [], 0), 0) # (state, path, cost), cost

    visited = {}   # using a dict to compare the costs of the visited

    while not fringe.isEmpty():

        state, path, current_cost = fringe.pop()

        if problem.isGoalState(state):
            return path
        
            # checking for the least cost state
        if state not in visited or visited[state] > current_cost:
            visited[state] = current_cost

            for successor, action, stepCost in problem.getSuccessors(state):
                new_cost = current_cost + stepCost
                new_path = path + [action]

                if successor not in visited or visited[successor] > new_cost:
                    fringe.push((successor, new_path, new_cost), new_cost)

    return []
 
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()

    start_state = problem.getStartState()

    # (first state, empty list for directions, cost g=0) priority = g+h , h=heuristic function
    fringe.push((start_state, [], 0), 0 + heuristic(start_state, problem))

    visited = {}

    while not fringe.isEmpty():
        state, path, current_cost = fringe.pop()

        if problem.isGoalState(state):
            return path

        if state not in visited or visited[state] > current_cost:
            visited[state] = current_cost

        for successor, action, stepCost in problem.getSuccessors(state):
                new_cost = current_cost + stepCost
                new_path = path + [action]

                priority = new_cost + heuristic(successor, problem)

                if successor not in visited or visited[successor] > new_cost:
                    visited[successor] = new_cost   # so we hold the cheapest path
                    fringe.push((successor, new_path, new_cost), priority)

    print("No solution found")
    return []

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

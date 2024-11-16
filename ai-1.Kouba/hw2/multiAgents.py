# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to" 
        "-NO"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        score = successorGameState.getScore()

        # let's find the smallest distance between pacman and the food 
        foodList = newFood.asList()
        if foodList:
            minFoodDistance = min([manhattanDistance(newPos, food)for food in foodList])
            # the closer, the higher the reward
            score += 10.0 / (minFoodDistance + 1)
        
        # get away from the ghosts
        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            # distance between Pacman and the ghost
            distanceToGhost = manhattanDistance(newPos, ghostPos)

            # if ghost are scared 
            if newScaredTimes[i] > 0:
                
                score += 200 / (distanceToGhost + 1)
            else:
                
                # large penalty for beeing too close to a ghost
                if distanceToGhost < 2:
                    score -= 1000
                else:
                    # small penalty for being not too close to a ghost
                    score -= 10.0 / (distanceToGhost + 1) 

        # small penalty for the rest of the food
        score -= len(foodList)

        # encourage collection of capsules
        capsules = successorGameState.getCapsules()
        if capsules:
            minCapsuleDistance = min(manhattanDistance(newPos, capsule) for capsule in capsules)
            score += 200.0 / (minCapsuleDistance + 1)

        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        legalMoves = gameState.getLegalActions(0)

        scores = [self.minimax(gameState.generateSuccessor(0, action), 0, 1) for action in legalMoves]

        bestScore = max(scores)

        bestIndex = scores.index(bestScore)

        return legalMoves[bestIndex]

    def minimax(self, state, depth, agentIndex):

        # if we find the max depth or end game there is no point to continue 
        if depth == self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        if agentIndex == 0:
            return max(self.minimax(state.generateSuccessor(agentIndex, action), depth, 1)for action in state.getLegalActions(agentIndex))

        # ghost turn
        else:
            nextAgent = agentIndex + 1
            if nextAgent >= state.getNumAgents():
                nextAgent = 0
                depth += 1

            return min(self.minimax(state.generateSuccessor(agentIndex, action), depth, nextAgent)
                       for action in state.getLegalActions(agentIndex))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        alpha = float("-inf")
        beta = float("inf")
        best_action = None
        max_value = float("-inf")

        # searching for the best pacman action 
        for action in gameState.getLegalActions(0):
            value = self.min_value(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if value > max_value:
                max_value = value
                best_action = action
            alpha = max(alpha, max_value)
        
        return best_action

    def max_value(self, gameState, depth, alpha, beta):
        # termination condition
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        value = float("-inf")
        for action in gameState.getLegalActions(0):
            value = max(value, self.min_value(gameState.generateSuccessor(0, action), 1, depth, alpha, beta))
            # pruning
            if value > beta:
                return value
            alpha = max(alpha, value)
        
        return value

    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        # termination condition (again)
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        value = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            # check if it is the last ghost, then go back to Pacman and increase the depth
            if agentIndex == gameState.getNumAgents() - 1:
                value = min(value, self.max_value(gameState.generateSuccessor(agentIndex, action), depth + 1, alpha, beta))
            else:
                value = min(value, self.min_value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta))
            
            # pruning
            if value < alpha:
                return value
            beta = min(beta, value)
        
        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        best_score = float("-inf")
        best_action = None

        # searching for the best pacman action (again)
        for action in gameState.getLegalActions(0):
            value = self.expectimax(gameState.generateSuccessor(0, action), 1, 0)
            if value > best_score:
                best_score = value
                best_action = action

        return best_action

    def expectimax(self, gameState, agentIndex, depth):
        
        # termination condition (again)
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # if Pacman plays (agentIndex = 0)
        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.exp_value(gameState, agentIndex, depth)

    def max_value(self, gameState, depth):
        
        value = float("-inf")
        for action in gameState.getLegalActions(0):
            value = max(value, self.expectimax(gameState.generateSuccessor(0, action), 1, depth))
        return value

    def exp_value(self, gameState, agentIndex, depth):
        
        actions = gameState.getLegalActions(agentIndex)
        if not actions:
            return self.evaluationFunction(gameState)

        total_value = 0
        probability = 1 / len(actions)

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            
            # if it is the last agent, we increase the depth
            if agentIndex == gameState.getNumAgents() - 1:
                total_value += probability * self.expectimax(successor, 0, depth + 1)
            else:
                total_value += probability * self.expectimax(successor, agentIndex + 1, depth)

        return total_value

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>

    <LET'S balance food eating, ghost avoidance, and capsule hunting.
    I reward Pacman for being close to food and capsules, while I penalize way too heavily
    for being close to active ghosts. If ghosts are scared, Pacman is
    wants to chase them of course. I also give a "tiny" penalty for
    remaining food, motivating Pacman to clear the board efficiently (just like a slave)>
    """

    "*** YOUR CODE HERE ***"

    score = currentGameState.getScore()

    # pos = position
    pacmanPos = currentGameState.getPacmanPosition()

    foodList = currentGameState.getFood().asList()

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # where is the closest food?
    if foodList:
        minFoodDistance = min(manhattanDistance(pacmanPos, food) for food in foodList)
        score += 10.0 / (minFoodDistance + 1)  # the closer to food the bigger the reward

    # where are the ghosts (in relation to pacman)
    for ghostIndex, ghostState in enumerate(ghostStates):
        ghostPos = ghostState.getPosition()
        distanceToGhost = manhattanDistance(pacmanPos, ghostPos)

        if scaredTimes[ghostIndex] > 0:
            # IT'S SCARED ATTACK
            score += 200 / (distanceToGhost + 1)
        else:
            # it's NOT scared... RUN
            if distanceToGhost < 2:
                score -= 1000 
            else:
                score -= 10.0 / (distanceToGhost + 1)  # I think we lost them but let's be sure about it

    capsules = currentGameState.getCapsules()
    if capsules:
        minCapsuleDistance = min(manhattanDistance(pacmanPos, capsule) for capsule in capsules)
        score += 100.0 / (minCapsuleDistance + 1) # make THEM run from YOU

    # c'mon it's your last "strength"
    score -= len(foodList) * 4

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

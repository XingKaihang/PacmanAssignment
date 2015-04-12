# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        if successorGameState.isWin():
          return float('inf')
        ghostPos = currentGameState.getGhostPositions()[0]
        ghostDis = manhattanDistance(ghostPos,newPos)
        score = max(ghostDis,2)*3 + successorGameState.getScore()

        remainFoods = 0
        nearestFoodDistance = float('inf')
        for food in newFood.asList():
          remainFoods += 1
          tmpDis = manhattanDistance(newPos,food)
          if tmpDis < nearestFoodDistance:
            nearestFoodDistance = tmpDis
        score -= 100*remainFoods
        score -= nearestFoodDistance*5

        return score
        #return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
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
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        curDepth = 0
        curAgentIndex = 0
        action = self.Max_Value(gameState, curDepth, curAgentIndex)
        return action[0]

    def Max_Value(self, gameState, curDepth, curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth :
        return self.evaluationFunction(gameState)

      v = float('-inf')
      finalAction = None
      for a in gameState.getLegalActions(curAgentIndex):
        if a == "Stop":
          continue
        tmpValue = self.Min_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
        if type(tmpValue) is tuple:
          tmpValue = tmpValue[1]
        v = max(v,tmpValue)
        if v == tmpValue:
          finalAction = a
      return (finalAction,v)

    def Min_Value(self, gameState, curDepth, curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth:
        return self.evaluationFunction(gameState)

      v = float('inf')
      finalAction = None
      if (curAgentIndex + 1) == gameState.getNumAgents():
        for a in gameState.getLegalActions(curAgentIndex):
          if a == "Stop":
            continue
          tmpValue = self.Max_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          v = min(v,tmpValue)
          if v == tmpValue:
            finalAction = a
      else:
        for a in gameState.getLegalActions(curAgentIndex):
          if a == "Stop":
            continue
          tmpValue = self.Min_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          v = min(v,tmpValue)
          if v == tmpValue:
            finalAction = a
      return (finalAction,v)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        curDepth = 0
        curAgentIndex = 0
        action = self.Max_Value(gameState, float('-inf'), float('inf'), curDepth, curAgentIndex)
        #print action[1]
        return action[0]

    def Max_Value(self, gameState,a,b,curDepth,curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth :
        return self.evaluationFunction(gameState)
      v = float('-inf')
      finalAction = None
      for action in gameState.getLegalActions(curAgentIndex):
        tmpValue = self.Min_Value( gameState.generateSuccessor(curAgentIndex,action), a, b, curDepth, curAgentIndex+1)
        if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
        v = max(v, tmpValue)
        if v > b:
          return (action, v)
        a = max(a,v)
        if v == tmpValue:
          finalAction = action
      return (finalAction,v)

    def Min_Value(self, gameState, a, b, curDepth, curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth:
        return self.evaluationFunction(gameState)
      finalAction = None
      v = float('inf')
      if (curAgentIndex + 1) == gameState.getNumAgents():
        #next one is max-value
        for action in gameState.getLegalActions(curAgentIndex):
          tmpValue = self.Max_Value(gameState.generateSuccessor(curAgentIndex,action), a, b, curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          v = min(v,tmpValue)
          if v < a:
            return (action,v)
          b = min(b,v) 
          if v == tmpValue:
            finalAction = action
      else:
        #next one is min-value
        for action in gameState.getLegalActions(curAgentIndex):
          tmpValue = self.Min_Value(gameState.generateSuccessor(curAgentIndex,action), a, b, curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          v = min(v,tmpValue)
          if v < a:
            return (action,v)
          b = min(b,v)
          if v == tmpValue:
            finalAction = action
      return (finalAction,v)        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        curDepth = 0
        curAgentIndex = 0
        action = self.Max_Value(gameState, curDepth, curAgentIndex)
        return action[0]

    def Max_Value(self, gameState, curDepth, curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth :
        return self.evaluationFunction(gameState)

      v = float('-inf')
      finalAction = None
      for a in gameState.getLegalActions(curAgentIndex):
        tmpValue = self.Average_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
        if type(tmpValue) is tuple:
          tmpValue = tmpValue[1]
        v = max(v,tmpValue)
        if v == tmpValue:
          finalAction = a
      return (finalAction,v)

    def Average_Value(self, gameState, curDepth, curAgentIndex):
      if curAgentIndex >= gameState.getNumAgents():
        curDepth += 1
        curAgentIndex = 0
      if gameState.isLose() or gameState.isWin() or curDepth == self.depth:
        return self.evaluationFunction(gameState)

      v = float('inf')
      sum_score = 0.0
      choice_number = 0

      if (curAgentIndex + 1) == gameState.getNumAgents():
        for a in gameState.getLegalActions(curAgentIndex):
          choice_number += 1
          tmpValue = self.Max_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          sum_score += tmpValue 
          
      else:
        for a in gameState.getLegalActions(curAgentIndex):
          choice_number += 1
          tmpValue = self.Average_Value(gameState.generateSuccessor(curAgentIndex,a), curDepth, curAgentIndex+1)
          if type(tmpValue) is tuple:
            tmpValue = tmpValue[1]
          sum_score += tmpValue 
      if choice_number == 0:
        return 0
      else:
        return sum_score/choice_number

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
      return float("inf")
    if currentGameState.isLose():
      return float("-inf")

    numghosts = currentGameState.getNumAgents() - 1
    i = 1
    disttoghost = float("inf")
    while i <= numghosts:
      nextdist = util.manhattanDistance(currentGameState.getPacmanPosition(), currentGameState.getGhostPosition(i))
      disttoghost = min(disttoghost, nextdist)
      i += 1

    score = max(disttoghost,2)*3 + currentGameState.getScore()
    remainFoods = 0
    nearestFoodDistance = float('inf')
    for food in newFood.asList():
      remainFoods += 1
      tmpDis = manhattanDistance(newPos,food)
      if tmpDis < nearestFoodDistance:
        nearestFoodDistance = tmpDis
    score -= 100*remainFoods
    score -= nearestFoodDistance*5
    capsulelocations = currentGameState.getCapsules()
    score -= 3.5 * len(capsulelocations)
    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


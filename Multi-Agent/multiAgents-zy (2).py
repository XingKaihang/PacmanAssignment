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





        oldFood = currentGameState.getFood() ## newFood should not be used to evaluate sucessor's value

        FoodList = oldFood.asList() 

        PacToFoodDisList = [] # create a list to store the manhattan distance from Pacman 
        # to the all the food
        for FoodPos in FoodList:
          PacToFoodDis = manhattanDistance(FoodPos, newPos)
          PacToFoodDisList.append(PacToFoodDis)
        PacToNearestFoodDis = min(PacToFoodDisList) # Record the distance from Pacman to 
        # the nearst food pellet
        #print PacToFoodDisList
        #print PacToNearestFoodDis

        #print newGhostStates
        #print successorGameState
        #newGhostPos = newGhostStates.getGhostPositions() is wrong because newGhostStates 
        #is a list not a state
        #newGhostPos = successorGameState.getGhostPositions()
        newGhostPos = currentGameState.getGhostPositions()
        #print newGhostPos
        PacToGhostDistList = []
        for GhostPos in newGhostPos:
          PacToGhostDis = manhattanDistance(GhostPos, newPos)
          PacToGhostDistList.append(PacToGhostDis)
        PacToNearestGhostDis = min(PacToGhostDistList)
        #print PacToGhostDistList
        #print PacToNearestFoodDis
        #print PacToNearestGhostDis
       

        if successorGameState.isWin():
            return 1
        if successorGameState.isLose(): # Pacman encounters the ghost. 
            return -1
        if PacToNearestFoodDis == 0:
            return PacToNearestGhostDis
        evalue = 1.0 / PacToNearestFoodDis - 1.0 / PacToNearestGhostDis
        return evalue
        "*** YOUR CODE HERE ***"
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
        agentNum = gameState.getNumAgents()
        Depth = agentNum * self.depth
        LegalActions = gameState.getLegalActions(0)


        #if Directions.STOP in LegalActions:
          #LegalActions.remove(Directions.STOP)

        ValueList = []
        for action in LegalActions:
          v = self.minimax(gameState.generateSuccessor(0, action), Depth -1  , 1, agentNum)
          #print v
          ValueList.append(v)
        #MaxValueInList = max(ValueList)
        #print ValueList
        FinalActionIndex = -1
        for i in range(len(LegalActions)):
          if ValueList[i] == max(ValueList):
            FinalActionIndex = i
            #print ValueList[i]
            break

        FinalAction = LegalActions[i]

        return FinalAction


    def minimax(self, gameState, depth, agentIndex, agentNum): 
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == 0 or len(legalActions) == 0:
          #print "!!!!!"
          return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
          maxv = -99999999
          for action in legalActions:
            v = self.minimax(gameState.generateSuccessor(agentIndex, action), depth-1, (agentIndex+1)%agentNum,agentNum)
            if v > maxv:
              maxv = v
          return maxv
        
        else:
          minv = 99999999
          if agentIndex == agentNum - 1:
             for action in legalActions:
                 v = self.minimax(gameState.generateSuccessor(agentIndex, action), depth-1, (agentIndex+1)%agentNum,agentNum)
                 minv = min(minv, v)
             return minv
          else:
             for action in legalActions:
                 v = self.minimax(gameState.generateSuccessor(agentIndex, action), depth-1, (agentIndex+1)%agentNum,agentNum)
                 minv = min(minv, v)
             return minv


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        agentNum = gameState.getNumAgents()
        Depth = agentNum * self.depth
        legalActions = gameState.getLegalActions(0)

        ValueList = []
        alpha = -999999
        beta = 999999
        for action in legalActions:
            v = self.Alpha_BetaValue(gameState.generateSuccessor(0,action), alpha, beta, Depth-1,1, agentNum)
            ValueList.append(v)
            alpha = max(alpha,max(ValueList))
          #print ValueList
          #print alpha


        FinalActionIndex = -1
     
        for i in range(len(legalActions)):
            if ValueList[i] == max(ValueList):
              FinalActionIndex =i
              break

        FinalAction = legalActions[i]
        return FinalAction 

    """
    def PrintCallStack(self):
      print "*callstack:"
      for line in traceback.format_stack():
          print line.strip()
    """

    def Alpha_BetaValue(self, gameState, alpha, beta, depth, agentIndex, agentNum):

        #self.PrintCallStack()
        legalActions = gameState.getLegalActions(agentIndex)

        if depth == 0 or len(legalActions) == 0:
            return self.evaluationFunction(gameState)
        if agentIndex == 0:#max
            maxv = -999999
            for action in legalActions:
              v = self.Alpha_BetaValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,depth-1,(agentIndex+1)%agentNum,agentNum)
              #print v
              if v > maxv:
                maxv = v            
              if maxv > beta:
                return maxv
              alpha  = max(alpha, maxv)
              #print "alpha=%d"% alpha
            return maxv
        else:#min
            minv = 999999
            for action in legalActions:
              v = self.Alpha_BetaValue(gameState.generateSuccessor(agentIndex,action),alpha,beta,depth-1,(agentIndex+1)%agentNum,agentNum)
              minv = min(minv,v)
              
              if minv < alpha:
                return minv
              beta = min(beta,minv)
              #print "beta= %f"% beta
              #print "alpha= %f"% alpha
            return minv
          



        util.raiseNotDefined()

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
        agentNum = gameState.getNumAgents()
        Depth = agentNum * self.depth
        legalActions = gameState.getLegalActions(0)

        ValueList=[]
        for action in legalActions:
            v = self.ExpectimaxValue(gameState.generateSuccessor(0,action),Depth-1,1,agentNum)
            ValueList.append(v)

        FinalActionIndex = -1
        for i in range(len(legalActions)):
            if ValueList[i] == max(ValueList):
              FinalActionIndex = i
              break

        FinalAction = legalActions[i]
        return FinalAction


    def ExpectimaxValue(self, gameState, depth, agentIndex, agentNum):
        legalActions = gameState.getLegalActions(agentIndex)
        if depth == 0 or len(legalActions) == 0:
          return self.evaluationFunction(gameState)
        if agentIndex == 0:
          maxv = -999999
          for action in legalActions:
            v = self.ExpectimaxValue(gameState.generateSuccessor(agentIndex,action), depth-1, (agentIndex+1)%agentNum, agentNum)
            if v > maxv:
              maxv = v
          return maxv

        else:
          sumv = float(0)
          for action in legalActions:
            v = self.ExpectimaxValue(gameState.generateSuccessor(agentIndex,action), depth-1, (agentIndex+1)%agentNum, agentNum)
            sumv = sumv + v
          mean = sumv/len(legalActions)
          return mean  

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    PacPos = currentGameState.getPacmanPosition()

    remainFoods = 0
    nearestFoodDistance = float('inf')
    for food in newFood.asList():
      remainFoods += 1
      tmpDis = manhattanDistance(newPos,food)
      if tmpDis < nearestFoodDistance:
        nearestFoodDistance = tmpDis

    
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")
    #if currentGameState.getLegalActions()

    #evalue = scoreEvaluationFunction(currentGameState) 
    evalue = scoreEvaluationFunction(currentGameState)-2*nearestFoodDistance - 100*RemairemainFoodsnFood

    return evalue


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


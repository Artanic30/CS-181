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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        return successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        PositiveInfinite = float("inf")
        NegativeInfinite = -float("inf")

        def get_max(state, cur_agent, depth):
            if state.isWin() or state.isLose():
                return state.getScore()

            if depth == self.depth:
                return self.evaluationFunction(state)

            result_score = NegativeInfinite

            actions = state.getLegalActions(cur_agent)
            final_action = "STOP"
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                sub_score = get_min(next_state, cur_agent + 1, depth)

                if sub_score > result_score:
                    result_score = sub_score
                    final_action = action

            if depth == 0:
                return final_action
            return result_score

        def get_min(state, cur_agent, depth):
            if state.isLose() or state.isWin():
                return state.getScore()

            total_agent = state.getNumAgents()
            result_score = PositiveInfinite

            actions = state.getLegalActions(cur_agent)
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                # last ghost
                if cur_agent == total_agent - 1:
                    sub_score = get_max(next_state, 0, depth + 1)
                else:
                    sub_score = get_min(next_state, cur_agent + 1, depth)

                if sub_score < result_score:
                    result_score = sub_score

            return result_score
        return get_max(gameState, 0, 0)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        PositiveInfinite = float("inf")
        NegativeInfinite = -float("inf")

        def get_max(state, cur_agent, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return state.getScore()

            if depth == self.depth:
                return self.evaluationFunction(state)

            result_score = NegativeInfinite

            actions = state.getLegalActions(cur_agent)
            final_action = "STOP"
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                sub_score = get_min(next_state, cur_agent + 1, depth, alpha, beta)

                if beta < sub_score:
                    return sub_score

                alpha = max(alpha, sub_score)

                if sub_score > result_score:
                    result_score = sub_score
                    final_action = action

            if depth == 0:
                return final_action
            return result_score

        def get_min(state, cur_agent, depth, alpha, beta):
            if state.isLose() or state.isWin():
                return state.getScore()

            total_agent = state.getNumAgents()
            result_score = PositiveInfinite

            actions = state.getLegalActions(cur_agent)
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                # last ghost
                if cur_agent == total_agent - 1:
                    sub_score = get_max(next_state, 0, depth + 1, alpha, beta)
                else:
                    sub_score = get_min(next_state, cur_agent + 1, depth, alpha, beta)
                beta = min(beta, sub_score)
                if sub_score < alpha:
                    return sub_score

                if sub_score < result_score:
                    result_score = sub_score

            return result_score

        return get_max(gameState, 0, 0, NegativeInfinite, PositiveInfinite)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        PositiveInfinite = float("inf")
        NegativeInfinite = -float("inf")

        def get_max(state, cur_agent, depth):
            if state.isWin() or state.isLose():
                return state.getScore()

            if depth == self.depth:
                return self.evaluationFunction(state)

            result_score = NegativeInfinite

            actions = state.getLegalActions(cur_agent)
            final_action = "STOP"
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                sub_score = get_min(next_state, cur_agent + 1, depth)

                if sub_score > result_score:
                    result_score = sub_score
                    final_action = action

            if depth == 0:
                return final_action
            return result_score

        def get_min(state, cur_agent, depth):
            if state.isLose() or state.isWin():
                return state.getScore()

            total_agent = state.getNumAgents()
            result_score = 0

            actions = state.getLegalActions(cur_agent)
            p = 1.0 / len(actions)
            for action in actions:
                next_state = state.generateSuccessor(cur_agent, action)
                # last ghost
                if cur_agent == total_agent - 1:
                    sub_score = get_max(next_state, 0, depth + 1)
                else:
                    sub_score = get_min(next_state, cur_agent + 1, depth)

                result_score += sub_score * p

            return result_score

        return get_max(gameState, 0, 0)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    ori_score = currentGameState.getScore()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()

    dis_ghost = 0
    for g in ghosts:
        dis = util.manhattanDistance(position, g.getPosition())
        if dis > 5:
            dis = 5
        dis = pow((-dis + 5), 8) * 1.0
        if g.scaredTimer > 0:
            dis_ghost += dis
        else:
            dis_ghost -= dis

    dis_food = 0
    for f in food:
        dis = util.manhattanDistance(position, f)
        if dis > 10:
            dis = 10
        dis = pow(-dis + 10, 4) * 1.0 / 750
        dis_food += dis

    ori_score += dis_ghost + dis_food

    # print(dis_ghost, dis_food, ori_score)
    return ori_score


# Abbreviation
better = betterEvaluationFunction

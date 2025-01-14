# bustersAgents.py
# ----------------
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


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters



class NullGraphics:
    "Placeholder for graphics"

    def initialize(self, state, isBlue=False):
        pass

    def update(self, state):
        pass

    def pause(self):
        pass

    def draw(self, state):
        pass

    def updateDistributions(self, dist):
        pass

    def finish(self):
        pass


class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observeUpdate(self, observation, gameState):
        noisyDistance = observation
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if noisyDistance != None and \
                    busters.getObservationProbability(noisyDistance, trueDistance) > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__(self, index=0, inference="ExactInference", ghostAgents=None, observeEnable=True,
                 elapseTimeEnable=True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        for index, inf in enumerate(self.inferenceModules):
            if not self.firstMove and self.elapseTimeEnable:
                inf.elapseTime(gameState)
            self.firstMove = False
            if self.observeEnable:
                inf.observe(gameState)
            self.ghostBeliefs[index] = inf.getBeliefDistribution()
        self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP


class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index=0, inference="KeyboardInference", ghostAgents=None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)


from distanceCalculator import Distancer
from game import Actions
from game import Directions


class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        """Pre-computes the distance between every two points."""
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closest to the closest ghost (according to mazeDistance!).
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i + 1]]
        "*** YOUR CODE HERE ***"
        closest_ghost = []
        for gh_dis in livingGhostPositionDistributions:
            max_prob = {
                "value": -1,
                "pos": None
            }
            for key, value in gh_dis.items():
                if value > max_prob["value"]:
                    max_prob = {
                        "value": value,
                        "pos": key
                    }
            closest_ghost.append(max_prob["pos"])

        closest_ghost.sort(key=lambda x: self.distancer.getDistance(x, pacmanPosition))
        target = closest_ghost[0]
        min_dis = {
            "value": 999999,
            "action": None
        }
        for action in legal:
            if action == Directions.NORTH:
                new_pos = pacmanPosition[0], pacmanPosition[1] + 1
                new_dis = self.distancer.getDistance(new_pos, target)
                if new_dis < min_dis["value"]:
                    min_dis = {
                        "value": new_dis,
                        "action": Directions.NORTH
                    }
            elif action == Directions.SOUTH:
                new_pos = pacmanPosition[0], pacmanPosition[1] - 1
                new_dis = self.distancer.getDistance(new_pos, target)
                if new_dis < min_dis["value"]:
                    min_dis = {
                        "value": new_dis,
                        "action": Directions.SOUTH
                    }
            elif action == Directions.EAST:
                new_pos = pacmanPosition[0] + 1, pacmanPosition[1]
                new_dis = self.distancer.getDistance(new_pos, target)
                if new_dis < min_dis["value"]:
                    min_dis = {
                        "value": new_dis,
                        "action": Directions.EAST
                    }
            elif action == Directions.WEST:
                new_pos = pacmanPosition[0] - 1, pacmanPosition[1]
                new_dis = self.distancer.getDistance(new_pos, target)
                if new_dis < min_dis["value"]:
                    min_dis = {
                        "value": new_dis,
                        "action": Directions.WEST
                    }
        return min_dis["action"]

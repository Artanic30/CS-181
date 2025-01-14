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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
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
    visited = []
    current_point = {
        "state": problem.getStartState(),
        "path": [],
    }
    process_stack = util.Stack()
    process_stack.push(current_point)

    while (not problem.isGoalState(current_point['state'])) or process_stack.isEmpty():
        current_point = process_stack.pop()

        if current_point['state'] in visited:
            continue

        visited.append(current_point['state'])

        if problem.isGoalState(current_point['state']):
            break

        tem_list = problem.getSuccessors(current_point['state'])
        if len(tem_list) != 0:
            for i in tem_list:
                potential_successor = i[0]
                if potential_successor not in visited:
                    process_stack.push({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                    })

    return current_point['path']


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = []
    current_point = {
        "state": problem.getStartState(),
        "path": [],
    }
    process_queue = util.Queue()
    process_queue.push(current_point)
    while (not problem.isGoalState(current_point['state'])) and not process_queue.isEmpty():
        current_point = process_queue.pop()

        if current_point['state'] in visited:
            continue

        visited.append(current_point['state'])

        if problem.isGoalState(current_point['state']):
            break

        tem_list = problem.getSuccessors(current_point['state'])
        if len(tem_list) != 0:
            for i in tem_list:
                potential_successor = i[0]
                if potential_successor not in visited:
                    process_queue.push({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                    })

    return current_point['path']



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    visited = []
    current_point = {
        "state": problem.getStartState(),
        "path": [],
        'cost': 0
    }
    process_pri_queue = util.PriorityQueue()
    process_pri_queue.push(current_point, current_point['cost'])

    while (not problem.isGoalState(current_point['state'])) and not process_pri_queue.isEmpty():
        current_point = process_pri_queue.pop()

        if current_point['state'] in visited:
            continue

        visited.append(current_point['state'])

        if problem.isGoalState(current_point['state']):
            break

        tem_list = problem.getSuccessors(current_point['state'])
        if len(tem_list) != 0:
            for i in tem_list:
                potential_successor = i[0]
                if potential_successor not in visited:
                    process_pri_queue.push({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                        'cost': i[2] + current_point['cost']
                    }, i[2] + current_point['cost'])
                else:
                    process_pri_queue.update({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                        'cost': i[2] + current_point['cost']
                    }, i[2] + current_point['cost'])

    return current_point['path']


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    current_point = {
        "state": problem.getStartState(),
        "path": [],
        'cost': 0
    }
    process_pri_queue = util.PriorityQueue()
    process_pri_queue.push(current_point, current_point['cost'] + heuristic(current_point["state"], problem))

    while (not problem.isGoalState(current_point['state'])) and not process_pri_queue.isEmpty():
        current_point = process_pri_queue.pop()

        if current_point['state'] in visited:
            continue

        visited.append(current_point['state'])

        if problem.isGoalState(current_point['state']):
            break

        tem_list = problem.getSuccessors(current_point['state'])
        if len(tem_list) != 0:
            for i in tem_list:
                potential_successor = i[0]
                if potential_successor not in visited:
                    process_pri_queue.push({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                        'cost': i[2] + current_point['cost']
                    }, i[2] + current_point['cost'] + heuristic(potential_successor, problem))
                else:
                    process_pri_queue.update({
                        'state': potential_successor,
                        "path": current_point['path'] + [i[1]],
                        'cost': i[2] + current_point['cost']
                    }, i[2] + current_point['cost'] + heuristic(potential_successor, problem))

    return current_point['path']


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

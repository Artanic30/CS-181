# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game
import re

pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'


class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()


def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")
    first = A | B
    # not_A = ~A
    second = ~A % ((~B) | C)
    third = logic.disjoin(~A, ~B, C)
    return logic.conjoin(first, second, third)


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")
    D = logic.Expr("D")
    first = C % (B | D)
    second = A >> logic.conjoin(~B, ~D)
    third = ~(B & (~C)) >> A
    fourth = ~D >> C
    return logic.conjoin(first, second, third, fourth)


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if (the Wumpus was alive at time 0 and it was
    not killed at time 0) or (it was not alive at time 0 and it was born at time 0).

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive0 = logic.PropSymbolExpr("WumpusAlive", 0)
    WumpusAlive1 = logic.PropSymbolExpr("WumpusAlive", 1)
    WumpusBorn0 = logic.PropSymbolExpr("WumpusBorn", 0)
    WumpusKilled0 = logic.PropSymbolExpr("WumpusKilled", 0)
    first = WumpusAlive1 % logic.disjoin(WumpusAlive0 & ~WumpusKilled0, ~WumpusAlive0 & WumpusBorn0)
    sec = ~(WumpusAlive0 & WumpusBorn0)
    third = WumpusBorn0
    return logic.conjoin(first, sec, third)


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    CNF_form = logic.to_cnf(sentence)
    return logic.pycoSAT(CNF_form)


def atLeastOne(literals):
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    result = None
    for ex in literals:
        if result:
            result = logic.disjoin(result, ex)
        else:
            result = ex
    return logic.to_cnf(result)


def atMostOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form) that represents the logic that at most one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = None
    for ex in literals:
        if result:
            result = logic.conjoin(result, ~ex)
        else:
            result = ~ex
    for i in range(len(literals)):
        tem_result = None
        for ex in literals:
            if literals.index(ex) != i:
                if tem_result:
                    tem_result = logic.conjoin(tem_result, ~ex)
                else:
                    tem_result = ~ex
            else:
                if tem_result:
                    tem_result = logic.conjoin(tem_result, ex)
                else:
                    tem_result = ex

        result = logic.disjoin(result, tem_result)
    return logic.to_cnf(result)


def exactlyOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form)that represents the logic that exactly one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = None
    for i in range(len(literals)):
        tem_result = None
        for ex in literals:
            if literals.index(ex) != i:
                if tem_result:
                    tem_result = logic.conjoin(tem_result, ~ex)
                else:
                    tem_result = ~ex
            else:
                if tem_result:
                    tem_result = logic.conjoin(tem_result, ex)
                else:
                    tem_result = ex
        if result:
            result = logic.disjoin(result, tem_result)
        else:
            result = tem_result
    return logic.to_cnf(result)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    result = []
    for key, value in model.items():
        if value:
            str_key = str(key)
            for action in actions:
                if action in str_key:
                    time = re.findall("[0-9]+", str_key)[0]
                    result.append((action, time))
    result.sort(key=lambda x: int(x[1]))
    return [i[0] for i in result]


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    result = logic.PropSymbolExpr(pacman_str, x, y, t)
    condition = None
    for action in [("South", (0, 1)), ("North", (0, -1)), ("East", (-1, 0)), ("West", (1, 0))]:
        x_cor = x + action[1][0]
        y_cor = y + action[1][1]
        if not walls_grid[x_cor][y_cor]:
            move = logic.Expr("{}[{}]".format(action[0], t - 1))
            state = logic.PropSymbolExpr(pacman_str, x_cor, y_cor, t - 1)
            if condition:
                condition = logic.disjoin(condition, move & state)
            else:
                condition = move & state
    return result % condition  # Replace this with your expression


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_pos = problem.getStartState()
    goal_pos = problem.getGoalState()

    result = [logic.PropSymbolExpr(pacman_str, start_pos[0], start_pos[1], 0), exactlyOne(
        [logic.PropSymbolExpr("North", 0), logic.PropSymbolExpr("South", 0), logic.PropSymbolExpr("East", 0),
         logic.PropSymbolExpr("West", 0)])]

    tick = 0
    try:
        while True:
            for col in range(1, width + 1):
                for row in range(1, height + 1):
                    if tick == 0:
                        if not (start_pos[0] == col and start_pos[1] == row) and not walls[col][row]:
                            result.append(~logic.PropSymbolExpr(pacman_str, col, row, 0))
                    else:
                        if not walls[col][row]:
                            result.append(pacmanSuccessorStateAxioms(col, row, tick, walls))
            result.append(exactlyOne(
                [logic.PropSymbolExpr("North", tick), logic.PropSymbolExpr("South", tick),
                 logic.PropSymbolExpr("East", tick),
                 logic.PropSymbolExpr("West", tick)]))

            result.append(pacmanSuccessorStateAxioms(goal_pos[0], goal_pos[1], tick + 1, walls))
            result.append(logic.PropSymbolExpr(pacman_str, goal_pos[0], goal_pos[1], tick + 1))
            tem_exp = None
            for ex in result:
                if tem_exp:
                    tem_exp = logic.conjoin(tem_exp, ex)
                else:
                    tem_exp = ex
            model = findModel(tem_exp)
            if model:
                return extractActionSequence(model, ["North", "South", "East", "West"])

            result = result[0:-2]
            tick += 1
            print(tick)
            # return ["West", "West", "West"]
    except:
        print("no result")
        exit(-1)


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_pos = problem.getStartState()[0]
    food_pos = problem.getStartState()[1]

    result = [logic.PropSymbolExpr(pacman_str, start_pos[0], start_pos[1], 0), exactlyOne(
        [logic.PropSymbolExpr("North", 0), logic.PropSymbolExpr("South", 0), logic.PropSymbolExpr("East", 0),
         logic.PropSymbolExpr("West", 0)])]

    tick = 0
    try:
        while True:
            for col in range(1, width + 1):
                for row in range(1, height + 1):
                    if tick == 0:
                        if not (start_pos[0] == col and start_pos[1] == row) and not walls[col][row]:
                            result.append(~logic.PropSymbolExpr(pacman_str, col, row, 0))
                    else:
                        if not walls[col][row]:
                            result.append(pacmanSuccessorStateAxioms(col, row, tick, walls))
            result.append(exactlyOne(
                [logic.PropSymbolExpr("North", tick), logic.PropSymbolExpr("South", tick),
                 logic.PropSymbolExpr("East", tick),
                 logic.PropSymbolExpr("West", tick)]))

            isGoal = []
            for col in range(1, width + 1):
                for row in range(1, height + 1):
                    if food_pos[col][row]:
                        tem = []
                        for t in range(0, tick + 1):
                            tem.append(logic.PropSymbolExpr(pacman_str, col, row, t))
                        if tem:
                            isGoal.append(atLeastOne(tem))
            length = len(isGoal)
            result += isGoal

            tem_exp = None
            for ex in result:
                if tem_exp:
                    tem_exp = logic.conjoin(tem_exp, ex)
                else:
                    tem_exp = ex
            model = findModel(tem_exp)
            if model:
                return extractActionSequence(model, ["North", "South", "East", "West"])

            result = result[0:-length]
            tick += 1
            print(tick)
            # return ["West", "West", "West"]
    except:
        print("no result")
        exit(-1)


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)

# Maxwell Carmichael - 11/1/2020, CS76 pa6

from ColoredMaze import ColoredMaze
from ColoredMazeRobot import ColoredMazeRobot
import numpy
from time import sleep
import random

class MazeHMMProblem:
    def __init__(self, mazefilename):
        random.seed(8)

        self.maze = ColoredMaze(mazefilename)
        self.robot = ColoredMazeRobot(self.maze)

        # maps sensor reading to probability distribution of each square giving the sensor reading
        self.sensormap = self.genSensorProbabilities()


        # generate first distribution, assuming we immediately get a reading upon placing the robot there
        self.currdistr = self.genInitialDistribution()

        # transition model
        self.transitionmodel = self.genTransitionModel()

        # method to call for moving the robot and updating probability distribution.
        # NOTE: the robot will start somewhere, but in animate() will not update its distribution until it moves somewhere else
    def step_and_filter(self):
        # step
        self.robot.step()

        # reading
        r = self.robot.getReading()

        # update probabilities after the step
        self.currdistr = self.filter(r)


        # given a reading, figure out where the robot could be now, conditional on previous probability distribution
    def filter(self, obs):
        sensor_model = self.sensormap[obs]  # probability of getting the reading given all possible current squares
        transition_model = self.transition(self.currdistr)  # current distribution, after considering transitions but before considering new evidence

        # get the updated model by pairwise multiplying the arrays, unequalized at first
        update = [a * b for a, b in zip(sensor_model, transition_model)]

        # figure out equalizing constant (to divide)
        alpha = 0
        for p in update:
            alpha += p

        # equalize
        for i in range(len(update)):
            update[i] /= alpha

        return update

        # method for generating probability distribution before any readings are done
    def genInitialDistribution(self):
        n = 0

        # count number of non-walls
        for square in self.maze.map:
            if square != '#':
                n += 1

        distr = []

        # set non-wall indices to 1/#walls
        for i in range(len(self.maze.map)):
            if self.maze.map[i] != '#':
                distr.append(1/n)
            else:
                distr.append(0.0)

        print(distr)
        return distr

        # returns { color : prob distribution of given reading for each square}
    def genSensorProbabilities(self):
        sensorProbs = { 'r' : [], 'g' : [], 'y' : [], 'b' : [] }

        for square in self.maze.map:
            if square == 'r':
                sensorProbs['r'].append(self.robot.pGood)
                sensorProbs['g'].append(self.robot.pBad)
                sensorProbs['y'].append(self.robot.pBad)
                sensorProbs['b'].append(self.robot.pBad)

            elif square == 'g':
                sensorProbs['r'].append(self.robot.pBad)
                sensorProbs['g'].append(self.robot.pGood)
                sensorProbs['y'].append(self.robot.pBad)
                sensorProbs['b'].append(self.robot.pBad)

            elif square == 'y':
                sensorProbs['r'].append(self.robot.pBad)
                sensorProbs['g'].append(self.robot.pBad)
                sensorProbs['y'].append(self.robot.pGood)
                sensorProbs['b'].append(self.robot.pBad)

            elif square == 'b':
                sensorProbs['r'].append(self.robot.pBad)
                sensorProbs['g'].append(self.robot.pBad)
                sensorProbs['y'].append(self.robot.pBad)
                sensorProbs['b'].append(self.robot.pGood)

            else: # wall
                sensorProbs['r'].append(0)
                sensorProbs['g'].append(0)
                sensorProbs['y'].append(0)
                sensorProbs['b'].append(0)

        print(sensorProbs)
        return sensorProbs

        # helper method which generates the transition model if robot is at a given location
    def genTransitionModelGivenLoc(self, x, y):
        if self.maze.map[self.maze.index(x, y)] == '#':
            return [0] * len(self.currdistr)  # impossible to be at a wall anyway

        # initialize current transition model given location
        transMGL = [0] * len(self.currdistr)

        # create a temporary robot at the location to generate all possible next moves
        mockRobot = ColoredMazeRobot(self.maze, (x, y))

        # for all possible moves from robot's location
        for move in mockRobot.genMoves():
            j = self.maze.index(move[0], move[1])  # index moved to with 1/4 probability

            transMGL[j] += 0.25

        return transMGL

        # method which generates the transition model for all locations
    def genTransitionModel(self):
        transM = []

        for i in range(len(self.currdistr)):
            loc = self.maze.to_tuple(i)

            transM.append(self.genTransitionModelGivenLoc(loc[0], loc[1]))

        print(transM)
        return transM

        # generate P(X_{t+1} | e_{1:t}), the probability distribution taking all evidence into account besides the current reading
    def transition(self, recursion):
        return numpy.matmul(recursion, self.transitionmodel)


        # given currdistr and the robot with a specific location, generate random moves and imperfect readings and animate each step
    def animate(self, n = 100):
        print("Initial location & probability distribution:")
        print(self.ASCII() + self.probDistrStr())

        i = 0
        while i < n:
            sleep(4)
            self.step_and_filter()
            print(self.ASCII() + self.probDistrStr())

            i += 1

        # returns maze as ASCII art
    def ASCII(self):
        robot_index = self.maze.index(self.robot.loc[0], self.robot.loc[1])

        str = ""

        for i in range(len(self.maze.map)):
            if i == robot_index:
                str += "~"
            elif self.maze.map[i] == '#':
                str += "#"
            else:
                str += self.maze.map[i]

            if (i + 1) % self.maze.width == 0:
                str += "\n"

        return str

        # put the current probability distribution into string form
    def probDistrStr(self):
        s = ""

        for i in range(len(self.maze.map)):
            p = str(round(self.currdistr[i], 3))  # round to 3 decimals

            while len(p) < 5:  # add zeroes to end
                p += "0"

            if self.currdistr[i] > 0.2:
                p += "*"
            else:
                p += " "

            if (i + 1) % self.maze.width == 0:
                s += p + "\n"
            else:
                s += p + "| "

        return s



if __name__ == "__main__":
    p = MazeHMMProblem("4x4.maz")
    p.animate()

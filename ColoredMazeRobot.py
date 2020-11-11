# Maxwell Carmichael - 11/1/2020
import random
from ColoredMaze import ColoredMaze

class ColoredMazeRobot:
    def __init__(self, maze, loc = None):
        self.maze = maze

        if loc:
            self.loc = loc
        else:
            # pick random start location uniformly
            starts = set()
            for i in range(maze.width):
                for j in range(maze.height):
                    if maze.is_floor(i, j):
                        starts.add((i, j))

            self.loc = random.choice(tuple(starts))

        self.pGood = 0.88  # Constant
        self.pBad = (1 - self.pGood) / 3  # pGood + 3*pBad = 1

        # move the robot, randomly uniformly in one of four directions
    def step(self):
        self.loc = random.choice(self.genMoves())  # equal likelihood of E, S, N, W

        # generates all possible moves given self.loc
    def genMoves(self):
        moves = list()  # set of possible moves
        # north
        moves.append(self.moveInDirection(0, 1))
        # south
        moves.append(self.moveInDirection(0, -1))
        # east
        moves.append(self.moveInDirection(1, 0))
        # west
        moves.append(self.moveInDirection(-1, 0))

        return moves

        # move helper method, returns new location after moving in x or y direction
    def moveInDirection(self, x, y):
        if self.maze.is_floor(self.loc[0] + x, self.loc[1] + y):
            return (self.loc[0] + x, self.loc[1] + y)
        else:
            return self.loc

        # get reading given self.loc, with the imperfect sensor
    def getReading(self):
        # list [correct, inc, inc, inc]
        posReadings = [self.maze.get_color(self.loc[0], self.loc[1])]  # correct color first

        # incorrects at indices 1, 2, 3
        if posReadings[0] != 'r':
            posReadings.append('r')
        if posReadings[0] != 'g':
            posReadings.append('g')
        if posReadings[0] != 'y':
            posReadings.append('y')
        if posReadings[0] != 'b':
            posReadings.append('b')

        # take a weighted random choice, and print if it was correct or not
        reading = random.choices(posReadings, weights = (self.pGood, self.pBad, self.pBad, self.pBad), k=1)[0]
        if reading == posReadings[0]:
            print("Correct reading: " + reading)
        else:
            print("Incorrect reading: " + reading)

        return reading

if __name__ == "__main__":
    test_maze1 = ColoredMaze("4x4.maz")
    robot1 = ColoredMazeRobot(test_maze1)
    print(robot1.loc)
    print(robot1.getReading())
    robot1.step()
    print(robot1.loc)
    print(robot1.getReading())
    robot1.step()
    print(robot1.loc)
    print(robot1.getReading())
    robot1.step()
    print(robot1.loc)
    print(robot1.getReading())

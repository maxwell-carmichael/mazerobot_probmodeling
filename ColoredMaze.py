# Maxwell Carmichael - CS 76. Reused some code from MazeWorld assignment.

class ColoredMaze:
    def __init__(self, mazefilename):
        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip() # gets rid of white space before & after
            # ignore blank limes
            if len(line) == 0:
                pass
            else:
                lines.append(line)
        f.close()

        self.width = len(lines[0])
        self.height = len(lines)

        # list, where index is that returned by self.index and value is a char representing color or wall
        self.map = list("".join(lines))


    # returns index in .map for a given coordiante
    def index(self, x, y):
        return (self.height - y - 1) * self.width + x

    # returns tuple in maze for a given index
    def to_tuple(self, i):
        x = i % self.width
        y = self.height - 1 - i // self.height
        return (x, y)

    # returns True if the location is a floor
    def is_floor(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        return self.map[self.index(x, y)] != '#'

    def get_color(self, x, y):
        if self.is_floor(x, y):
            return self.map[self.index(x,y)]
        else:
            return None


            
# Some test code

if __name__ == "__main__":
    test_maze1 = ColoredMaze("4x4.maz")
    print(test_maze1.map)
    print(test_maze1.get_color(1, 0))

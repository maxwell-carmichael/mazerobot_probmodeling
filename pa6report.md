Maxwell Carmichael

Professor Alberto Quattrini Li
###### CS76 - PA6: Hidden Markov Models

### Introduction
In this programming assignment, I implemented a filtering algorithm to predict the locations of a robot moving randomly about an *n* x m maze, with colored tiles (red, yellow, green, blue) and walls, and the only information the robot has to predict its location is an imperfect color sensor aimed at the floor.

### Description
##### ColoredMaze
The first step in designing the algorithm is to create a class which reads .maz files. Here, I reused Maze.py from pa2, removing anything that referenced the locations of the current robots, keeping the conversion of the maze to list form, keeping the is_floor and index functions, and adding a get_color function which returns the color of the maze at a given (x, y) location.

I made the design decision that my program could handle any rectangular maze, not just 4x4 ones.

##### ColoredMazeRobot
The next design implementation I decided was necessary was to have an object representing the robot, which moves about the maze randomly and contains a sensor which provides imperfect readings. It has a ColoredMaze object as an instance variable to help with this, and also has two constants pGood and pBad, which represent the probability of an accurate reading and the probability of getting a specific wrong reading. I set these to 0.88 and 0.04 respectively (as the programming assignment specifies), but they may be changed if desired.

##### MazeHMMProblem
This class is the main problem-solver. It contains the filtering algorithm and the animate method, and it will initialize the ColoredMaze and a ColoredMazeRobot object.

The filtering algorithm is entirely based on the following equation, from the textbook:
<img src="eq14.5.png">

The sensor model is easy to generate, as there will only be four different sensor models corresponding to each of the four color readings. If (0, 0) has a red tile, and our evidence is red, there will be a 0.88 probability of getting this evidence given we are on (0, 0). If our evidence is yellow, there will be a 0.04 probability of getting this evidence. As you can see, no complex math is necessary to generate the sensor models for the four different evidence readings.

The following codeblock is a test maze and the corresponding sensor models for the four possible readings. The lists read left to right, top to bottom.
```
grby
yr#r
#rgy
rbyr

{
'r': [0.04, 0.88, 0.04, 0.04, 0.04, 0.88, 0, 0.88,
0, 0.88, 0.04, 0.04, 0.88, 0.04, 0.04, 0.88],
'g': [0.88, 0.04, 0.04, 0.04, 0.04, 0.04, 0, 0.04,
0, 0.04, 0.88, 0.04, 0.04, 0.04, 0.04, 0.04],
'y': [0.04, 0.04, 0.04, 0.88, 0.88, 0.04, 0, 0.04,
0, 0.04, 0.04, 0.88, 0.04, 0.04, 0.88, 0.04],
'b': [0.04, 0.04, 0.88, 0.04, 0.04, 0.04, 0, 0.04,
 0, 0.04, 0.04, 0.04, 0.04, 0.88, 0.04, 0.04]}
```

The "recursion" is already generated, and is stored as the current probability distribution (which we will update afterwards). The initial "recursion" is the probability distribution with no readings, which is generated with the genInitialDistribution method. Here, all non-wall tiles have an equal probability of starting with the robot.

The transition model, like the sensor model, can be generated once and used indefinitely, as the maze never changes. I represent the transition model as an *n* x *n* matrix, with *n* being the number of tiles of the maze. The rows represent all the probability distributions of the robot's locations given that it was at a specific location. Thus, if A is the transition matrix, the entry A<sub>ij</sub> is the probability the robot ends up at location j after being at location i.


To sum the transitioned probability distributions over the possible locations of the robot, take the recursion list as a 1 x *n* matrix and the transition model as an *n* x *n* matrix, and matrix multiply them to generate a 1 x *n* **transitioned list**, which represents the possible current locations given the robot took a step but **without** updating with our new evidence. For some intuition on why this works, consider an entry of the transitioned list. We find this by taking the probability the robot reaches this location given a previous location (transition model) and multiplying it by our previous probability the robot was at this location (recursion/previous probability distribution), and summing these numbers over all possible previous locations. The matrix multiplication does exactly this, to compute every entry of the transitioned list.

The final step, since we have our transitioned list, is to update this transitioned list based on the sensor reading, which we can do simply by pairwise multiplying the items in the sensor model and the items in the transitioned list. After normalizing these probabilities, we have our new probability distribution.


This class also contains an animate method which takes the number of steps we want our robot to take as a parameter. Note that here we assume the robot gets its first reading *after* it moves for the first time. It prints the maze and robot location (seen as "~"), and the probability distribution, with asterisks for probabilities greater than 0.2.

### Analysis
For the following maze,
```
grby
yr#r
#rgy
rbyr
```
The following is some code output from animating MazeHMMProblem, with ~ as the location of the robot. Remember that the robot does not take readings until after it moves for the first time.
```
Initial location & probability distribution:
grby
yr#r
#~gy
rbyr
0.071 | 0.071 | 0.071 | 0.071
0.071 | 0.071 | 0.000 | 0.071
0.000 | 0.071 | 0.071 | 0.071
0.071 | 0.071 | 0.071 | 0.071

(1)
Incorrect reading: b
grby
yr#r
#r~y
rbyr
0.018 | 0.018 | 0.393*| 0.018
0.018 | 0.018 | 0.000 | 0.018
0.000 | 0.018 | 0.018 | 0.018
0.018 | 0.393*| 0.018 | 0.018

(2)
Correct reading: y
grby
yr#r
#rgy
rb~r
0.003 | 0.017 | 0.032 | 0.381*
0.061 | 0.003 | 0.000 | 0.003
0.000 | 0.017 | 0.003 | 0.061
0.017 | 0.017 | 0.381*| 0.003

(3)
Correct reading: g
grby
yr#r
#r~y
rbyr
0.119 | 0.004 | 0.030 | 0.052
0.008 | 0.006 | 0.000 | 0.029
0.000 | 0.003 | 0.658*| 0.004
0.004 | 0.028 | 0.026 | 0.029
```

An obvious thing to note is that (0, 1) and (2, 2) always have a probability of zero, which makes sense, as these spaces have walls. The first reading on (2, 1) is an incorrect blue reading, and you can see that the algorithm thinks that the robot is likely to be on one of the two blue tiles. The second reading is correct, and the algorithm this time does give a high probability that the robot is at its true location, quickly recovering after the incorrect reading. The third reading gives a 65.8\% probability the robot is at its true location, which makes sense, as this is the only square which can be reached by the sequence of the first three readings, 'b', 'y', and 'g'.

```
(4)
Correct reading: y
grby
yr#r
#rgy
rb~r
0.006 | 0.004 | 0.003 | 0.087
0.076 | 0.001 | 0.000 | 0.003
0.000 | 0.017 | 0.017 | 0.386*
0.001 | 0.001 | 0.397*| 0.002

(5)
Correct reading: y
grby
yr#r
#rgy
rb~r
0.003 | 0.000 | 0.003 | 0.139
0.123 | 0.003 | 0.000 | 0.017
0.000 | 0.001 | 0.029 | 0.315*
0.000 | 0.015 | 0.323*| 0.028

(6)
Correct reading: g
grby
yr#r
#r~y
rbyr
0.138 | 0.001 | 0.007 | 0.014
0.012 | 0.006 | 0.000 | 0.023
0.000 | 0.002 | 0.708*| 0.019
0.001 | 0.016 | 0.019 | 0.033

(7)
Correct reading: r
grby
yr#r
#~gy
rbyr
0.011 | 0.122 | 0.001 | 0.002
0.006 | 0.017 | 0.000 | 0.065
0.000 | 0.591*| 0.027 | 0.029
0.015 | 0.001 | 0.028 | 0.084
```

In the same way, the remaining correct readings up to and including (7) yield probabilities that continue to make sense. For instance, from (3) to (4), we have a high probability the robot is on (2, 1), and then we get a reading of 'y'. There are two yellow tiles adjacent to (2, 1), thus it makes sense that these two tiles have the highest probabilities for the robot's true location.

```
(8)
Incorrect reading: r
grby
yr#r
#rgy
r~yr
0.003 | 0.074 | 0.003 | 0.002
0.001 | 0.359*| 0.000 | 0.078
0.000 | 0.311*| 0.015 | 0.005
0.023 | 0.014 | 0.003 | 0.110

(9)
Correct reading: r
grby
yr#r
#rgy
~byr
0.002 | 0.181 | 0.002 | 0.002
0.007 | 0.306*| 0.000 | 0.067
0.000 | 0.288*| 0.006 | 0.004
0.034 | 0.007 | 0.003 | 0.094

(10)
Correct reading: r
grby
yr#r
#rgy
~byr
0.004 | 0.205*| 0.004 | 0.001
0.006 | 0.326*| 0.000 | 0.058
0.000 | 0.253*| 0.006 | 0.003
0.045 | 0.006 | 0.002 | 0.081

(11)
Correct reading: b
grby
yr#r
#rgy
r~yr
0.015 | 0.036 | 0.314*| 0.004
0.023 | 0.053 | 0.000 | 0.008
0.000 | 0.040 | 0.018 | 0.010
0.009 | 0.452*| 0.006 | 0.011
```

At (8) we get another incorrect reading, and we can see that the probabilities do not "recover" until step (11).

"""Launch a number of balls with random direction and wheel velocities.

Expects number of balls to launch as command line argument.
"""

import time
import random
import sys

import ball_launcher.ball_launcher_control as bl

if len(sys.argv) != 2:
    print("Please provide number of balls to launch as command line argument.")

else:
    n_balls = int(sys.argv[1])
    launcher = bl.BallLauncher()

    for i in range(n_balls):
        phi = random.random()
        theta = random.random()
        top_left_motor = random.uniform(0.2, 1.0)
        top_right_motor = random.uniform(0.2, 1.0)
        bottom_motor = random.uniform(0.2, 1.0)

        launcher.set_state(phi, theta, top_left_motor, top_right_motor, bottom_motor)
        launcher.launch_ball()

        time.sleep(2)

"""Launch a number of balls with random direction and wheel velocities.

Expects number of balls to launch as command line argument.
"""

import time
import random
import sys

import ball_launcher as bl

if len(sys.argv) != 2:
    print("Please provide number of balls to launch as command line argument.")

else:
    n_balls = int(sys.argv[1])
    launcher = bl.BallLauncher()

    for i in range(n_balls):
        phi = random.random()
        theta = random.random()
        top_vel = random.uniform(0.2, 1.0)
        bottom_vel = random.uniform(0.2, 1.0)

        launcher.set_state(phi, theta, top_vel, bottom_vel)
        launcher.launch_ball()

        time.sleep(2)

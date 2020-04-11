"""Launch 2^2 balls with extreme orientations, i.e. each servo of the launcher is
either at its minimum or maximum value.
"""

import time
import itertools

import ball_launcher as bl

launcher = bl.BallLauncher()

ang_vel = ((0.5, 0.5))

for orientation in itertools.product(*[[0., 1.]]*2):
    launcher.set_state(*(orientation + ang_vel))
    launcher.launch_ball()

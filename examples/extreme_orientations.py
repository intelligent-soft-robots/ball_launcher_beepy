"""Launch 2^2 balls with extreme orientations, i.e. each servo of the launcher is
either at its minimum or maximum value.
"""

import time
import itertools

import ball_launcher as bl

launcher = bl.BallLauncher()

motor = ((0.3, 0.3, 0.3))

for orientation in itertools.product(*[[0., 1.]]*2):
    launcher.set_state(*(orientation + motor))
    launcher.launch_ball()

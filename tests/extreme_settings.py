"""Launch 2^4 balls with extreme settings, i.e. each parameter of the launcher is
either at its minimum or maximum value.
"""

import time
import itertools

import ball_launcher as bl

launcher = bl.BallLauncher()

for orientation in itertools.product(*[[0., 1.]]*2):
	for ang_vel in itertools.product(*[[0.2, 1.]]*2):
	    launcher.set_state(*(orientation + ang_vel))
	    launcher.launch_ball()

"""Launch 2^4 balls with extreme settings, i.e. each parameter of the launcher is
either at its minimum or maximum value.
"""

import time
import itertools

import ball_launcher as bl

launcher = bl.BallLauncher()

for orientation in itertools.product(*[[0., 1.]]*2):
	for motor in itertools.product(*[[0.2, 1.]]*3):
	    launcher.set_state(*(orientation + motor))
	    launcher.launch_ball()

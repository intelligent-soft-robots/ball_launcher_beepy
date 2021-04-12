"""Launch 2^5 balls with extreme settings, i.e. each parameter of the launcher is
either at its minimum or maximum value. NOTE: Balls might be fast!
"""

import time
import itertools

import ball_launcher.ball_launcher_control as bl

launcher = bl.BallLauncher()

for orientation in itertools.product(*[[0., 1.]]*2):
	for motor in itertools.product(*[[0.2, 1.]]*3):
	    launcher.set_state(*(orientation + motor))
	    launcher.launch_ball()

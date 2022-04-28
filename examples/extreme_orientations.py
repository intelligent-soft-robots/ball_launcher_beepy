"""Launch 2^2 balls with extreme orientations, i.e. each servo of the launcher is
either at its minimum or maximum value.
"""

import time
import itertools

from ball_launcher_beepy.ball_launcher_control import BallLauncher

launcher = BallLauncher()

motor = (0.3, 0.3, 0.3)

for orientation in itertools.product(*[[0.0, 1.0]] * 2):
    launcher.set_state(*(orientation + motor))
    launcher.launch_ball()

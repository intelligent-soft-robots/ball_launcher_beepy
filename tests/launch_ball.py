"""Set up ball launcher and launch one ball.

Expects azimuthal angle (phi) and altitude of angle (theta) 
of launcher and angular velocity of top and bottom wheels as 
command line argument, i.e., four floating point numbers in the 
range (0, 1) where 0 is minimal and 1 is maximal. Note: At an 
angular velocity of 0 the wheels don't turn at all and hence 
the ball won't be launched. """

import time
import sys

import ball_launcher.ball_launcher_control as bl

if len(sys.argv) != 5:
    print("Please provide azimuthal angle (phi) and altitude of angle (theta) of launcher and angular velocity of top and bottom wheels as command line arguments.") 

else:
    phi = float(sys.argv[1])
    theta = float(sys.argv[2])
    top_ang_vel = float(sys.argv[3])
    bottom_ang_vel = float(sys.argv[4])

    launcher = bl.BallLauncher(
        phi = phi,
	theta = theta,
	top_ang_vel = top_ang_vel,
	bottom_ang_vel = bottom_ang_vel)

    launcher.launch_ball()

    time.sleep(1)

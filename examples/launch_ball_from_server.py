"""Set up ball launcher and launch one ball.

Expects azimuthal angle (phi) and altitude of angle (theta)
of launcher and motor activation of all three wheels as
command line argument, i.e., five floating point numbers in the
range (0, 1) where 0 is minimal and 1 is maximal. Note: At a
motor activation of 0 the wheels don't turn at all and hence
the ball won't be launched. """

import argparse

from ball_launcher_beepy.ball_launcher_control import BallLauncher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phi", type=float, help="Azimuthal angle of launcher head.")
    parser.add_argument("theta", type=float, help="Altitude angle of launcher head.")
    parser.add_argument(
        "top_left_motor", type=float, help="Activation of top left motor."
    )
    parser.add_argument(
        "top_right_motor", type=float, help="Activation of top right motor."
    )
    parser.add_argument("bottom_motor", type=float, help="Activation of bottom motor.")
    args = parser.parse_args()

    launcher = BallLauncher()

    launcher.set_state(
        phi=args.phi,
        theta=args.theta,
        top_left_motor=args.top_left_motor,
        top_right_motor=args.top_right_motor,
        bottom_motor=args.bottom_motor,
    )
    launcher.launch_ball()

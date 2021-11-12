"""Start client, send set state request and then launch ball request to ball launcher server. 

Expects IP address of server and port number as command line arguments."""

import argparse
from time import sleep
#import ball_launcher.ball_launcher_client as ball_launcher_client
from ball_launcher_beepy import BallLauncherClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start client, send set state request and then launch ball request to ball launcher server.")
    parser.add_argument("ip", type=str, help="IP address of ball launcher server.")
    parser.add_argument("port", type=str, help="Port number of ball launcher server.")
    parser.add_argument("phi", type=float, help="Azimuthal angle of launcher head.")
    parser.add_argument("theta", type=float, help="Altitude angle of launcher head.")
    parser.add_argument("top_left_motor", type=float, help="Activation of top left motor.")
    parser.add_argument("top_right_motor", type=float, help="Activation of top right motor.")
    parser.add_argument("bottom_motor", type=float, help="Activation of bottom motor.")
    args = parser.parse_args()

    client = BallLauncherClient(args.ip, args.port)
    client.set_state(
        phi=args.phi,
        theta=args.theta,
        top_left_motor=args.top_left_motor,
        top_right_motor=args.top_right_motor,
        bottom_motor=args.bottom_motor
    )
    sleep(1)
    client.launch_ball()

"""Run ball launcher server which starts listening to requests from clients and executes their commands. 

Expects port number as command line argument."""

import argparse

import ball_launcher.ball_launcher_server as ball_launcher_server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ball launcher server.")
    parser.add_argument("port", type=str, help="Port number of ball launcher server.")
    args = parser.parse_args()

    server = ball_launcher_server.BallLauncherServer(args.port)
    server.run()

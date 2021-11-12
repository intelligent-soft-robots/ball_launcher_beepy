#!/usr/bin/env python3

"""
Starts the ball launcher server on port 5555
"""

from ball_launcher_beepy import BallLauncherServer

if __name__ == "__main__":
    server = BallLauncherServer(5555)
    server.run()


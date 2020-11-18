"""Run ball launcher server which starts listening to requests from clients and executes their commands. 

Expects port number as command line argument."""


import sys

import ball_launcher_beepy.ball_launcher_server as ball_launcher_server

if len(sys.argv) != 2:
    print("Please provide port number as command line argument.") 
else:
    port = int(sys.argv[1])
    server = ball_launcher_server.BallLauncherServer(port)

    server.run()


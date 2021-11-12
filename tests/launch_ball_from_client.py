"""Start client, send set state request and then launch ball request to ball launcher server. 

Expects IP address of server and port number as command line arguments."""


import sys

import ball_launcher_beepy.ball_launcher_client as ball_launcher_client

if len(sys.argv) != 3:
    print("Please provide IP address and port number as command line arguments.") 
else:
    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    client = ball_launcher_client.BallLauncherClient(ip_address, port)

    client.set_state(
            phi = 0.5, 
            theta = 0.5, 
            top_ang_vel = 0.3, 
            bottom_ang_vel = 0.4)

    client.launch_ball()

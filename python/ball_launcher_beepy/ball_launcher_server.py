import zmq

import ball_launcher_pb2
import ball_launcher.ball_launcher_control as ball_launcher_control

class BallLauncherServer:
    """Server waiting for commands for the ball launcher. Uses ZeroMQ for communication with clients. Uses BallLauncher 
    object for control of ball launcher."""

    def __init__(self, port_number):
        """Set up ball launcher server. Expects port number."""

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(port_number))

        # BallLauncher object that controls servos. Initialized at neutral orientation, wheels at rest.
        self.launcher = ball_launcher_control.BallLauncher()
        
    def run(self):
        """Run server which starts to listen to messages from clients containing requests for the ball launcher."""

        while True:
            # Wait for next request from client
            message = self.socket.recv()

            request = ball_launcher_pb2.Request()

            try:
                # Process message using protobuf
                request.ParseFromString(message)

                # Use ball launcher to realize request
                if request.request == ball_launcher_pb2.Request.RequestType.SET_STATE:
                    self.launcher.set_state(
                            phi = request.state.phi,
                            theta = request.state.theta,
                            top_ang_vel = request.state.top_ang_vel,
                            bottom_ang_vel = request.state.bottom_ang_vel)
                elif request.request == ball_launcher_pb2.Request.RequestType.LAUNCH_BALL:
                    self.launcher.launch_ball()
                else:
                    raise Exception("Ball launcher server: Unknown request type: {}".format(request.request))

            except:
                self.socket.send(b"0")
            else:
                self.socket.send(b"1")


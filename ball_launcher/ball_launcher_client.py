import zmq

import ball_launcher_pb2

class BallLauncherClient:
    """Client sending commands to the ball launcher. Uses ZeroMQ for communication with server."""

    def __init__(self, ip_address, port_number):
        """Set up ball launcher client. Expects ip address of server as string and port number."""

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        print("tcp://{}:{}".format(ip_address, port_number))
        self.socket.connect("tcp://{}:{}".format(ip_address, port_number))

        
    def set_state(self, phi, theta, top_ang_vel, bottom_ang_vel):
        """Set orientation of launcher and motor speeds.
        
        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_ang_vel -- angular velocity of upper wheel (in [0, 1])
        bottom_ang_vel -- angular velocity of lower wheel (in [0, 1])
        """

        # communicate request to server using protobuf
        request = ball_launcher_pb2.Request()

        request.request = ball_launcher_pb2.Request.RequestType.SET_STATE
        request.state.phi = phi
        request.state.theta = theta
        request.state.top_ang_vel = top_ang_vel
        request.state.bottom_ang_vel = bottom_ang_vel

        self.socket.send(request.SerializeToString())

        # Get the reply
        message = self.socket.recv()
        if message == "0":
            raise Exception("Ball launcher server failed to process SET_STATE request.")

    def launch_ball(self):
        """Launch single ball."""
        # communicate request to server using protobuf
        request = ball_launcher_pb2.Request()
        request.request = ball_launcher_pb2.Request.RequestType.LAUNCH_BALL

        self.socket.send(request.SerializeToString())

        # Get the reply
        message = self.socket.recv()
        if message == "0":
            raise Exception("Ball launcher server failed to process LAUNCH_BALL request.")




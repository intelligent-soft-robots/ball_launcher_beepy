from ball_launcher_beepy import BallLauncherClient



class BallLauncher:

    """
    Context manager for a BallLauncherClient. Ensures the motor velocities
    are set back to 0.
    All arguments values as values between 0 and 1 (except for ip and port)
    Args:
        ip, port : of the server (installed on the ball launcher Rasperri Pi)
        phi : azimutal angle of the launch pad
        theta : altitute angle of the launch pad
        top_left_motor: activation of the top left motor
        top_right_motor: activation of the top right motor
        bottom_motor: activation of the bottom motor
    """
    
    def __init__(
            self,
            ip: str,
            port: int,
            phi: float,
            theta: float,
            top_left_motor: float,
            top_right_motor: float,
            bottom_motor: float
    ):

        self._client = BallLauncherClient(ip, port)
        self._phi = phi
        self._theta = theta
        self._top_left_motor = top_left_motor
        self._top_right_motor = top_right_motor
        self._bottom_motor = bottom_motor


    def __enter__(self) -> BallLauncherClient:
        self._client.set_state
        (
            self._phi,
            self._theta,
            self._top_left_motor,
            self._top_right_motor,
            self._bottom_motor
        )
        return self._client

    def __exit__(self,exc_type,exc_value,exc_traceback):
        """
        Set the motors velocities to 0
        """
        self._client.set_state
        (
            self._phi,
            self._theta,
            0.,
            0.,
            0.
        )
        

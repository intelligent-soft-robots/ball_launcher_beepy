from .ball_launcher_client import BallLauncherClient
from .ball_launcher import BallLauncher
try:
    from .ball_launcher_server import BallLauncherServer 
except ModuleNotFoundError as e:
    # if not on the server raspberry pi, the modules required 
    # for the server may be missing. This is fine because most
    # certainly only the client will be needed. 
    # But if the user tries to start a server, informing him/her
    # why this fails.
    class BallLauncherServer:
        def __init__(self, _):
            raise Exception("Fails to start the server because of missing module: {}".format(e))

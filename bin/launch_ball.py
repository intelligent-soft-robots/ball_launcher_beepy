#!/usr/bin/env python3

"""
Connects to ball launcher beepy and send a ball.
The ball launcher server should be running on the 
raspberry pi of the ball launcher.
"""

import typing
from ball_launcher_beepy import BallLauncher


class _BallLauncherConfig:
    def __init__(self):
        # reasonable default values
        self.ip = "10.42.31.174"
        self.port = 5555
        self.phi = 0.5
        self.theta = 0.5
        self.top_left_motor = 0.5
        self.top_right_motor = 0.5
        self.bottom_motor = 0.5


def _dialog() -> _BallLauncherConfig:
    """
    Configuration dialog, provides reasonable default
    values.
    """
    config = _BallLauncherConfig()

    args = (
        ("ip", str),
        ("port", int),
        ("phi", float),
        ("theta", float),
        ("top_left_motor", float),
        ("top_right_motor", float),
        ("bottom_motor", float),
    )

    def _get_user_input(arg: str, type_:typing.Union[str,int,float], config: _BallLauncherConfig) -> bool:
        # returns None if keyboard interrupt, user entered value otherwise
        ok = False
        while not ok:
            value = input(
                str("\tvalue for {} ({}): ").format(arg, getattr(config, arg))
            )
            if value=="":
                # user pressed enter, using default value
                value=getattr(config,arg)
            try:
                value = type_(value)
                ok = True
            except ValueError:
                print("\t\terror, could not cast to", type_)
            except KeyboardInterrupt:
                return None
        return value

    for arg, type_ in args:
        value = _get_user_input(arg, type_, config)
        if value is None:
            return None
        else:
            setattr(config,arg,value)

    return config


def _launch(config: _BallLauncherConfig) -> None:
    """
    Does send the ball according to the provided
    configuration
    """
    with BallLauncher(
        config.ip,
        config.port,
        config.phi,
        config.theta,
        config.top_left_motor,
        config.top_right_motor,
        config.bottom_motor,
    ) as client:
        client.launch_ball()


def _execute():

    print()
    config = _dialog()
    if config != None:
        _launch(config)
    print()


if __name__ == "__main__":
    """
    Starts a configuration dialog, then
    send a ball according to the provided configuration.
    """
    _execute()
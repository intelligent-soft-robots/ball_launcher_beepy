import json
import numpy as np
import os
import time

from xOC05 import xOC05
from xOC03 import xOC03 # TODO: Why do we import a module for a second servo driver?


class BallLauncher:
    """Control of the ball launcher. Handles setting of PWM signals."""

    def __init__(self, phi=0.5, theta=0.5, top_left_motor=0., top_right_motor=0., 
            bottom_motor=0., config_path=None):
        """Set up ball launcher by initializing PCA9685 controller and setting 
        initial values for duty cycle of PWM signals. 
        
        Arguments:
        phi -- initial azimuthal angle of launcher (in [0, 1], default 0.5)
        theta -- initial altitude of launcher (in [0, 1], default 0.5)
        top_left_motor -- initial activation of top left motor (in [0, 1], default 0.0)
        top_left_motor -- initial activation of top right motor (in [0, 1], default 0.0)
        bottom_motor -- initial activation of bottom motor (in [0, 1], default 0.0)
        config_path -- Path to configuration file. If None, the path 
            "~/.ball_launcher_config.json" is used.
        """

        # load config file
        if config_path is None:
            path = os.path.expanduser("~/.ball_launcher_config.json")
        else:
            path = config_path
        with open(path, "r") as file:
            self.conf = json.load(file)

        # initialize servo motor drivers
        self.servo_driver1 = xOC03()
        self.servo_driver1.init()
        self.servo_driver2 = xOC05()
        self.servo_driver2.init(50) # 50 is probably frequency in Hz?

        self.set_state(phi, theta, top_left_motor, top_right_motor, bottom_motor)

        # open ball supply initially
        self._set_off_ticks("ball_supply", 0.0)

        # initial position of stirrer
        self._set_off_ticks("stirrer", 0.0)

        # TODO: What does this do?
        self.servo_driver1.writePin(True)

    def __del__(self):
        """Switch off motors and go to neutral orientation."""

        self.set_state(0.5, 0.5, 0., 0., 0.)
        self._set_off_ticks("stirrer", 0.0)

        # TODO: What does this do?
        self.servo_driver1.writePin(False)

    def set_state(self, phi, theta, top_left_motor=0., top_right_motor=0., 
            bottom_motor=0.):
        """Set orientation of launcher and motor speeds.
        
        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_left_motor -- activation of top left motor (in [0, 1], default 0.0)
        top_left_motor -- activation of top right motor (in [0, 1], default 0.0)
        bottom_motor -- activation of bottom motor (in [0, 1], default 0.0)
        """

        self.phi = np.clip(phi, 0., 1.)
        self.theta = np.clip(theta, 0., 1.)
        self.top_left_motor = np.clip(top_left_motor, 0., 1.)
        self.top_right_motor= np.clip(top_right_motor, 0., 1.)
        self.bottom_motor= np.clip(bottom_motor, 0., 1.)

        self._set_off_ticks("phi", self.phi)
        self._set_off_ticks("theta", self.theta)
        self._set_off_ticks("top_left_motor", self.top_left_motor, motor=True)
        self._set_off_ticks("top_right_motor", self.top_right_motor, motor=True)
        self._set_off_ticks("bottom_motor", self.bottom_motor, motor=True)

        time.sleep(self.T_SLEEP)

    def launch_ball(self):
        """Launch single ball."""

        # stir balls
        self._set_off_ticks("stirrer", 1.0)

        # wait for ball to fall down in pipe
        time.sleep(self.conf["times"]["t_ball_fall"])  

        # close and push one ball to wheels
        self._set_off_ticks("ball_supply", 1.0)
        # TODO: Why is it necessary to call setServoPosition repeatedly?
        for tick in np.range(self.conf["ticks"]["ball_supply"][0] + 3, 
                             self.conf["ticks"]["ball_supply"][1], 3):
            self.servo_driver2.setServoPosition(self.conf["channels"]["ball_supply"], tick)

        # retract rod
        self._set_off_ticks("ball_supply", 0.0)

        # reset stirrer
        self._set_off_ticks("stirrer", 0.0)

        # TODO: Should there be a sleep time here to ensure that wheels get up 
        # to speed again after transferring energy to ball? Otherwise 
        # shooting in rapid succession would alter the velocity of the ball.

    def _set_off_ticks(self, quantity, value, motor=False):
        """Set tick value (integers) for end of pulse for PWM signal.
        
        Arguments:
        quantity -- name of the channel to be modified (see config file)
        value -- value in [0, 1] which interpolates between min and max off tick
        motor -- boolean indicating whether this is channel attached to a motor
        """
        v = np.clip(value, 0., 1.)
        channel = self.conf["channel"][quantity]
        if motor:
            motor_ticks = self.conf["ticks"]["motor"]
            motor_offset = self.conf["ticks"][quantity + "_offset"]
            ticks = [t + offset for t, offset in zip(motor_ticks, motor_offset)]
        else:
            ticks = self.conf["ticks"][quantity]
        tick = round((1. - v)*ticks[0] + v*ticks[1])
        self.servo_driver2.setServoPosition(channel, tick)

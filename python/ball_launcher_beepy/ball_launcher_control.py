import json
import logging
import os
import threading
import typing
import warnings

import numpy as np
from scipy.interpolate import interp1d

from RPi import GPIO
from xOC03 import xOC03  # TODO: Why do we import a module for a second servo driver?
from xOC05 import xOC05


class BallLauncherControl:
    """Control of the ball launcher. Handles setting of PWM signals."""

    def __init__(
        self,
        phi: float = 0.5,
        theta: float = 0.5,
        top_left_motor: float = 0.0,
        top_right_motor: float = 0.0,
        bottom_motor: float = 0.0,
        config_path: typing.Optional[str] = None,
    ) -> None:
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
        self.servo_driver2.init(50)  # 50 is probably frequency in Hz?

        self.set_state(phi, theta, top_left_motor, top_right_motor, bottom_motor)

        # open ball supply initially
        self._set_off_ticks("ball_supply_push", 0.0)

        # initial position of stirrer
        self._set_off_ticks("stirrer", 0.0)

        # TODO: What does this do?
        self.servo_driver1.writePin(True)

        try:
            # automatic motor reset after launching
            self.automatic_motor_reset = bool(
                self.conf["launching_parameters"]["automatic_motor_reset"]
            )
            self.stirring_after_launch = bool(
                self.conf["launching_parameters"]["stirring_after_launch"]
            )
        except KeyError as e:
            logging.error(f"Configuration does not contain parameters. {e}")

        # initialize GPIO ports for stirr sensor if configured
        self._stirr_sensor_available = False

        if "stirr_sensor" in self.conf["channels"]:
            self._stirr_sensor_available = True
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.conf["channels"]["stirr_sensor"], GPIO.IN)

        self.set_state(0.5, 0.5, 0.0, 0.0, 0.0)
        self.launcher_ready_flag = True

    def __del__(self) -> None:
        """Switches off motors and sets orientation to neutral."""

        self.set_state(0.5, 0.5, 0.0, 0.0, 0.0)
        self._set_off_ticks("stirrer", 0.0)

        # TODO: What does this do?
        self.servo_driver1.writePin(False)

    def set_state(
        self,
        phi: float,
        theta: float,
        top_left_motor: float = 0.0,
        top_right_motor: float = 0.0,
        bottom_motor: float = 0.0,
    ) -> None:
        """Set orientation of launcher and motor speeds.

        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_left_motor -- activation of top left motor (in [0, 1], default 0.0)
        top_left_motor -- activation of top right motor (in [0, 1], default 0.0)
        bottom_motor -- activation of bottom motor (in [0, 1], default 0.0)
        """

        self.phi = np.clip(phi, 0.0, 1.0)
        self.theta = np.clip(theta, 0.0, 1.0)
        self.top_left_motor = np.clip(top_left_motor, 0.0, 1.0)
        self.top_right_motor = np.clip(top_right_motor, 0.0, 1.0)
        self.bottom_motor = np.clip(bottom_motor, 0.0, 1.0)

        self._set_off_ticks("phi", self.phi)
        self._set_off_ticks("theta", self.theta)
        self._set_off_ticks("top_left_motor", self.top_left_motor, motor=True)
        self._set_off_ticks("top_right_motor", self.top_right_motor, motor=True)
        self._set_off_ticks("bottom_motor", self.bottom_motor, motor=True)

    def set_rpm(
            self,
            phi: float,
            theta: float,
            rpm_top_left: float,
            rpm_top_right: float,
            rpm_bottom_center: float
    ):
        set_flag = True

        rpm_tl = self.conf["rpm_conversion"]["rpm_tl"]
        rpm_tr = self.conf["rpm_conversion"]["rpm_tr"]
        rpm_bc = self.conf["rpm_conversion"]["rpm_bc"]
        actuation = self.conf["rpm_conversion"]["actuation"]

        rpm_list = [rpm_top_left, rpm_top_right, rpm_bottom_center]

        # sets interpolation limits
        minimum_rpm = float(max([min(rpm_tr), min(rpm_tl), min(rpm_bc)]))
        maximum_rpm = float(min([max(rpm_tr), max(rpm_tl), max(rpm_bc)]))

        for rpm in rpm_list:
            if minimum_rpm > rpm > maximum_rpm:
                warnings.warn("Given speed cannot be set. Set is ommitted.")
                set_flag = False

        if set_flag:
            f_tl = interp1d(rpm_tl, actuation)
            f_tr = interp1d(rpm_tr, actuation)
            f_bc = interp1d(rpm_bc, actuation)

            actuation_top_left = f_tl(rpm_top_left)
            actuation_top_right = f_tr(rpm_top_right)
            actuation_bottom_center = f_bc(rpm_bottom_center)

            self.set_state(
                phi=phi,
                theta=theta,
                top_left_motor=actuation_top_left,
                top_right_motor=actuation_top_right,
                bottom_motor=actuation_bottom_center,
            )

    def launch_ball(self) -> None:
        """Launches ball. Resets rod position of crank mechanism for ball supply
        after time specified in configuration file."""

        def _timed_reset_stirring() -> None:
            """Timed function for reseting stirring."""
            # reset stirrer
            self._set_off_ticks("stirrer", 0.0)

        def _timed_launching() -> None:
            """Timed function for delayed launching."""
            self._set_off_ticks("ball_supply_push", 0.0)
            for tick in np.arange(
                self.conf["ticks"]["ball_supply_push"][0],
                self.conf["ticks"]["ball_supply_push"][1],
                self.conf["launching_parameters"]["ball_supply_stroke_gain"],
            ):
                self.servo_driver2.setServoPosition(
                    self.conf["channels"]["ball_supply_push"], tick
                )
            self.launcher_ready_flag = False

        def _timed_reset_ball_supply() -> None:
            """Timed function for reseting / retracting ball supply rod."""
            self._set_off_ticks("ball_supply_push", 0.0)
            self.launcher_ready_flag = True

        if self.stirring_after_launch:
            # stir balls
            self._set_off_ticks("stirrer", 1.0)

            # delayed reset of stirring
            stirring_time = self.conf["times"]["t_stirring"]
            stirr_timer = threading.Timer(stirring_time, _timed_reset_stirring)
            stirr_timer.start()

        if self.launcher_ready_flag:
            # close and push one ball to wheels
            t_launch_delay = self.conf["times"]["t_launch_delay"]
            launch_timer = threading.Timer(t_launch_delay, _timed_launching)
            launch_timer.start()

            # resets crank mechanism of ball supply unit
            t_supply_reset = self.conf["times"]["t_supply_reset"]
            t_supply_reset += t_launch_delay
            supply_timer = threading.Timer(t_supply_reset, _timed_reset_ball_supply)
            supply_timer.start()

        if self.automatic_motor_reset:
            # turns motors off after launch
            t_reset_motors = self.conf["times"]["t_reset_motors"]
            t_reset_motors += t_supply_reset
            motor_reset_timer = threading.Timer(
                t_reset_motors, self.set_state, [self.phi, self.theta, 0.0, 0.0, 0.0]
            )
            motor_reset_timer.start()

    def _set_off_ticks(self, quantity: str, value: float, motor: bool = False) -> None:
        """Set tick value (integers) for end of pulse for PWM signal.

        Arguments:
        quantity -- name of the channel to be modified (see config file)
        value -- value in [0, 1] which interpolates between min and max off tick
        motor -- boolean indicating whether this is channel attached to a motor
        """
        v = np.clip(value, 0.0, 1.0)
        channel = self.conf["channels"][quantity]
        if motor:
            motor_ticks = self.conf["ticks"]["motor"]
            motor_offset = self.conf["ticks"][quantity + "_offset"]
            ticks = [t + offset for t, offset in zip(motor_ticks, motor_offset)]
        else:
            ticks = self.conf["ticks"][quantity]
        tick = round(ticks[0] + v * (ticks[1] - ticks[0]))

        self.servo_driver2.setServoPosition(channel, tick)

    def check_ball_supply(self) -> None:
        """Continuously checking ball supply sensor and sets stirring."""
        if self._stirr_sensor_available:
            if not GPIO.input(self.conf["channels"]["stirr_sensor"]):
                # reset stirrer
                self._set_off_ticks("stirrer", 0.0)
            else:
                # stir balls
                self._set_off_ticks("stirrer", 1.0)

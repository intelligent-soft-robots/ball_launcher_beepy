import numpy as np
import time

import Adafruit_PCA9685

class BallLauncher:
    """Control of the ball launcher. Handles setting of PWM signals."""

    # channels used in servo driver
    PHI_CH = 8 # azimuthal angle of launcher
    THETA_CH = 9 # altitude of launcher
    TOP_ANG_VEL_CH = 10 # angular velocity of upper wheel
    BOTTOM_ANG_VEL_CH = 11 # angular velocity of  lower wheel
    BALL_SUPPLY_CH = 14 # pushes ball towards wheels
    STIRRER_CH = 15 # stirs ball in funnel

    # max and min values for "off" tick value of pulse
    PHI_TICK_MAX = 400
    PHI_TICK_MIN = 250
    THETA_TICK_MAX = 320
    THETA_TICK_MIN = 180

    TOP_ANG_VEL_TICK_MAX = 380
    TOP_ANG_VEL_TICK_MIN = 200
    BOTTOM_ANG_VEL_TICK_MAX = 380
    BOTTOM_ANG_VEL_TICK_MIN = 200

    BALL_SUPPLY_PUSH_TICK1 = 160 # open
    BALL_SUPPLY_PUSH_TICK2 = 440

    # an off tick value 0 switches stirrer off,
    # a low value makes it turn left,
    # and high value makes it turn right.
    # At about 330 servo doesn't turn.
    STIRRER_REST = 0 # stop
    STIRRER_LEFT = 220 # 
    STIRRER_RIGHT = 420

    # time to sleep after changing PWM signal in order to give system time
    # to reach a stationary configuration. TODO: Adjust if necessary
    T_SLEEP = 1.5

    # time for the ball to fall to bottom of pipe in seconds
    T_BALL_FALL = 1.5

    # time for the stirrer to turn from one position to the other in seconds
    T_STIRRER = 1.0
    

    def __init__(self, phi = 0.5, theta = 0.5, top_ang_vel = 0., bottom_ang_vel = 0.):
        """Set up ball launcher by initializing PCA9685 controller and setting 
        initial values for duty cycle of PWM signals. 
        
        Arguments:
        phi -- initial azimuthal angle of launcher (in [0, 1], default 0.5)
        theta -- initial altitude of launcher (in [0, 1], default 0.5)
        top_ang_vel -- initial angular velocity of upper wheel (in [0, 1], default 0.0)
        bottom_ang_vel -- initial angular velocity of lower wheel (in [0, 1], default 0.0)
        """

        # initialise the PCA9685 using the default address (0x70).
        self.pca = Adafruit_PCA9685.PCA9685(address=0x70)

        #TODO: 50Hz or 60Hz? Ask Heiko
        # set frequency to 60hz, good for servos
        self.pca.set_pwm_freq(50)

        self.set_state(phi, theta, top_ang_vel, bottom_ang_vel)

        # close ball supply initiialy
        self.pca.set_pwm(self.BALL_SUPPLY_CH, 0, self.BALL_SUPPLY_PUSH_TICK2) 

    def __del__(self):
        """Switch off motors and go to neutral orientation."""
        self.set_state(0.5, 0.5, 0., 0.)
        self.pca.set_pwm(self.STIRRER_CH, 0, self.STIRRER_REST)
        self.pca.set_pwm(self.BALL_SUPPLY_CH, 0, self.BALL_SUPPLY_PUSH_TICK2) # closed
        

    def set_state(self, phi, theta, top_ang_vel, bottom_ang_vel):
        """Set orientation of launcher and motor speeds.
        
        Arguments:
        phi -- azimuthal angle of launcher (in [0, 1])
        theta -- altitude of launcher (in [0, 1])
        top_ang_vel -- angular velocity of upper wheel (in [0, 1])
        bottom_ang_vel -- angular velocity of lower wheel (in [0, 1])
        """
        self.phi = np.clip(phi, 0., 1.)
        self.theta = np.clip(theta, 0., 1.)
        self.top_ang_vel = np.clip(top_ang_vel, 0., 1.)
        self.bottom_ang_vel = np.clip(bottom_ang_vel, 0., 1.)

        self._set_launcher_off_ticks(
                round((1. - phi)*self.PHI_TICK_MIN + phi*self.PHI_TICK_MAX),
                round((1. - theta)*self.THETA_TICK_MIN + theta*self.THETA_TICK_MAX),
                round((1. - top_ang_vel)*self.TOP_ANG_VEL_TICK_MIN + top_ang_vel*self.TOP_ANG_VEL_TICK_MAX),
                round((1. - bottom_ang_vel)*self.BOTTOM_ANG_VEL_TICK_MIN + bottom_ang_vel*self.BOTTOM_ANG_VEL_TICK_MAX))

    def launch_ball(self):
        """Launch single ball."""

        # retract rod
        self.pca.set_pwm(self.BALL_SUPPLY_CH, 0, self.BALL_SUPPLY_PUSH_TICK1) # open

        # wait for ball to fall down in pipe
        time.sleep(self.T_BALL_FALL)  

        # stir balls
        self.pca.set_pwm(self.STIRRER_CH, 0, self.STIRRER_LEFT)
        time.sleep(self.T_STIRRER)
        self.pca.set_pwm(self.STIRRER_CH, 0, self.STIRRER_RIGHT)
        time.sleep(self.T_STIRRER)
        self.pca.set_pwm(self.STIRRER_CH, 0, self.STIRRER_REST)

        # close and push one ball to wheels
        self.pca.set_pwm(self.BALL_SUPPLY_CH, 0, self.BALL_SUPPLY_PUSH_TICK2) 
        time.sleep(self.T_SLEEP)


    def _set_launcher_off_ticks(self, phi_servo, theta_servo, top_motor, bottom_motor):
        """Set tick values (integers) for end of pulse for PWM signals concerning the head of the launcher.
        
        Arguments:
        phi_servo -- tick value for azimuthal angle (in PHI_TICK_MIN..PHI_TICK_MAX])
        theta_servo -- tick value for altitude (in THETA_TICK_MIN..THETA_TICK_MAX])
        top_motor -- tick value for speed of upper wheel (in TOP_ANG_VEL_TICK_MIN..TOP_ANG_VEL_TICK_MAX])
        bottom_motor -- tick value for speed of upper wheel (in BOTTOM_ANG_VEL_TICK_MIN..BOTTOM_ANG_VEL_TICK_MAX])
        """
        self.pca.set_pwm(self.PHI_CH, 0, int(np.clip(phi_servo, self.PHI_TICK_MIN, self.PHI_TICK_MAX)))
        self.pca.set_pwm(self.THETA_CH, 0, int(np.clip(theta_servo, self.THETA_TICK_MIN, self.THETA_TICK_MAX)))
        self.pca.set_pwm(self.TOP_ANG_VEL_CH, 0, int(np.clip(top_motor, self.TOP_ANG_VEL_TICK_MIN, self.TOP_ANG_VEL_TICK_MAX)))
        self.pca.set_pwm(self.BOTTOM_ANG_VEL_CH, 0, int(np.clip(bottom_motor, self.BOTTOM_ANG_VEL_TICK_MIN, self.BOTTOM_ANG_VEL_TICK_MAX)))
        time.sleep(self.T_SLEEP)




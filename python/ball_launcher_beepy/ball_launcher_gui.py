import logging
import time
import tkinter as tk

from RPi import GPIO
from xOC03 import xOC03
from xOC05 import xOC05


class BallLauncherGUI:
    def __init__(
        self, root: tk.Tk, ports: dict, driver_interface_oc05, driver_interface_oc03
    ) -> None:
        root.winfo_screenwidth()
        root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (800, 400))
        root.config(bg="grey")

        root.start_time = time.time()
        root.mixer_first_run_flag = True

        self.root = root
        self.ports = ports
        self.driver_interface_oc05 = driver_interface_oc05
        self.driver_interface_oc03 = driver_interface_oc03

        # initial value for ball feeding unit
        self.ball_feeder_endposition = 180

        # control parameters
        self.checkup_delay = 2000  # [ms]
        self.error_delay = 10.0  # [s]

        # Tkinter slider for motor and orientation control
        class SliderThrowingMotors:
            def __init__(self, title, X, Y, port, gain):
                def motor_soll(val):
                    motor_speed = int(val)
                    motor_speed += gain
                    print(f"Turning speed {title}: {motor_speed}")
                    driver_interface_oc05.setServoPosition(port, motor_speed)

                self.slider = tk.Scale(
                    root,
                    from_=150,
                    to=30,
                    orient=tk.VERTICAL,
                    length=200,
                    width=50,
                    bg="grey",
                    bd=5,
                    font=("Arial", 16),
                    fg="yellow",
                    sliderlength=50,
                    troughcolor="yellow",
                    command=motor_soll,
                )
                self.slider.place(x=X, y=Y)

                self.title = tk.Label(
                    root, text=title, font=("Arial", 14), bg="grey", fg="yellow"
                )
                self.title.place(x=X + 10, y=Y - 25)

        class SliderVerticalPosition:
            def __init__(self, title, X, Y, port):
                def servo_vertical_soll(val):
                    serpos = int(val)
                    print(f"Servo vertical: {serpos}")
                    driver_interface_oc05.setServoPosition(port, serpos)

                self.slider = tk.Scale(
                    root,
                    from_=150,
                    to=30,
                    orient=tk.VERTICAL,
                    length=200,
                    width=50,
                    bg="grey",
                    bd=5,
                    font=("Arial", 16),
                    fg="green",
                    sliderlength=50,
                    troughcolor="green",
                    command=servo_vertical_soll,
                )
                self.slider.set(90)
                self.slider.place(x=X, y=Y)

                self.title = tk.Label(
                    root, text=title, font=("Arial", 12), bg="grey", fg="green"
                )
                self.title.place(x=X + 10, y=Y - 25)

        class SliderHorizontalPosition:
            def __init__(self, title, X, Y, port):
                def servo_horizontal_soll(val):
                    serpos = int(val)
                    print(f"Servo horizontal: {serpos}")
                    driver_interface_oc05.setServoPosition(port, serpos)

                self.slider = tk.Scale(
                    root,
                    from_=30,
                    to=150,
                    orient=tk.HORIZONTAL,
                    length=455,
                    width=50,
                    bg="grey",
                    bd=5,
                    font=("Arial", 16),
                    fg="blue",
                    sliderlength=50,
                    troughcolor="blue",
                    command=servo_horizontal_soll,
                )
                self.slider.set(90)
                self.slider.place(x=X, y=Y)

                self.title = tk.Label(
                    root, text=title, font=("Arial", 12), bg="grey", fg="blue"
                )
                self.title.place(x=X + 10, y=Y - 25)

        # initialisation slider throwing motors
        SliderThrowingMotors("Motor TR", 360, 25, self.ports["motor_top_right"], 0)
        SliderThrowingMotors("Motor TL", 150, 25, self.ports["motor_top_left"], 0)
        SliderThrowingMotors("Motor BC", 255, 25, self.ports["motor_bottom_center"], 0)

        # initialisation slider orientation actuators
        SliderHorizontalPosition("Left/Right", 0, 300, self.ports["servo_horizontal"])
        SliderVerticalPosition("Up/Down", 0, 25, self.ports["servo_vertical"])

        # Tkinter button for launching and counter modification
        btn_shoot = tk.Button(
            root,
            bd=4,
            bg="#00FF99",
            text="Multiball",
            font=("Arial", 14, "bold"),
            command=self.launch_multiple_balls,
        )

        btn_add_ball = tk.Button(
            root,
            bd=4,
            bg="#00FF00",
            text="+1",
            font=("Arial", 10, "bold"),
            command=self.add_ball,
        )

        btn_add_multiple_balls = tk.Button(
            root,
            bd=4,
            bg="#AAFF00",
            text="+10",
            font=("Arial", 10, "bold"),
            command=self.add_multiple_balls,
        )

        btn_remove_ball = tk.Button(
            root,
            bd=4,
            bg="#006600",
            text="-1",
            font=("Arial", 10, "bold"),
            command=self.remove_ball,
        )

        btn_remove_multiple_balls = tk.Button(
            root,
            bd=4,
            bg="#666600",
            text="-10",
            font=("Arial", 10, "bold"),
            command=self.remove_multiple_balls,
        )

        btn_close = tk.Button(
            root,
            bd=4,
            bg="#D6992F",
            text="EXIT",
            font=("Arial", 20, "bold"),
            command=self.close,
        )

        btn_single_shot = tk.Button(
            root,
            bd=4,
            bg="#0CC3F8",
            text="SINGLE SHOT",
            font=("Arial", 18, "bold"),
            command=self.launch_ball,
        )

        btn_shoot.place(x=510, y=170, width=120, height=120)
        btn_add_ball.place(x=630, y=170, width=60, height=40)
        btn_add_multiple_balls.place(x=690, y=170, width=60, height=40)
        btn_remove_ball.place(x=630, y=250, width=60, height=40)
        btn_remove_multiple_balls.place(x=690, y=250, width=60, height=40)
        btn_close.place(x=510, y=310, width=250, height=80)
        btn_single_shot.place(x=510, y=30, width=250, height=120)

        # Tkinter label for ball counter display
        self.lb_n_balls = tk.Label(
            root, bd=4, bg="#009900", font=("Arial", 10, "bold"), text="0"
        )

        self.lb_n_balls.place(x=630, y=210, width=120, height=40)

        # run sensor loop
        root.after(self.checkup_delay, self.sensor_loop)

    # close interface
    def stop_motors(self):
        self.driver_interface_oc05.setServoPosition(self.ports["motor_top_right"], 30)
        self.driver_interface_oc05.setServoPosition(self.ports["motor_top_left"], 30)
        self.driver_interface_oc05.setServoPosition(
            self.ports["motor_bottom_center"], 30
        )
        self.driver_interface_oc05.setServoPosition(
            self.ports["mixer"], 102
        )  # neutral position servo

    def close(self):
        self.stop_motors()

        self.driver_interface_oc03.writePin(False)
        time.sleep(0.2)
        self.root.destroy()

    # launching interface
    def launch_ball(self):
        """Launches ball with parameters set via sliders."""
        self.driver_interface_oc05.setServoPosition(self.ports["servo_ball_feeder"], 30)
        self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 180)
        time.sleep(0.5)  # default 0.5
        servo_gain = 0
        while servo_gain <= self.ball_feeder_endposition:
            servo_gain += 1.5
            self.driver_interface_oc05.setServoPosition(
                self.ports["servo_ball_feeder"], servo_gain
            )
        else:
            self.driver_interface_oc05.setServoPosition(
                self.ports["servo_ball_feeder"], 30
            )
            self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 102)

    # multi-shot specification
    def add_ball(self):
        """Increments multi-shot counter by 1."""
        value = int(self.lb_n_balls["text"])
        self.lb_n_balls["text"] = f"{value + 1}"
        multi_ball = value + 1
        print(f"+1 Multi Ball: {multi_ball}")

    def add_multiple_balls(self):
        """Increments multi-shot counter by 10."""
        value = int(self.lb_n_balls["text"])
        self.lb_n_balls["text"] = f"{value + 10}"
        multi_ball = value + 10
        print(f"+10 Multi Ball: {multi_ball}")

    def remove_ball(self):
        """Decrements multi-shot counter by 1."""
        value = int(self.lb_n_balls["text"])
        if value != 0:
            self.lb_n_balls["text"] = f"{value - 1}"
            multi_ball = value - 1
            print(f"-1 Multi Ball: {multi_ball}")

    def remove_multiple_balls(self):
        """Decrements multi-shot counter by 10."""
        value = int(self.lb_n_balls["text"])
        if value >= 10:
            self.lb_n_balls["text"] = f"{value - 10}"
            multi_ball = value - 10
            print(f"-10 Multi Ball: {multi_ball}")

    def launch_multiple_balls(self):
        """Launches number of balls specified in multi-shot counter."""
        counter = int(self.lb_n_balls["text"])
        logging.debug(f"Multi-shot counter: {counter}")
        while counter != 0:
            counter = counter - 1
            self.driver_interface_oc05.setServoPosition(
                self.ports["servo_ball_feeder"], 30
            )
            self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 180)
            time.sleep(0.5)
            servo_gain = 0
            while servo_gain <= self.ball_feeder_endposition:
                servo_gain += 0.5
                self.driver_interface_oc05.setServoPosition(
                    self.ports["servo_ball_feeder"], servo_gain
                )
            else:
                self.driver_interface_oc05.setServoPosition(
                    self.ports["servo_ball_feeder"], 30
                )
                self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 102)

    # Loop for checking ball supply sensor.
    def sensor_loop(self, stirrer_pin):
        """Checks state of filling sensor and activates reservoir stirrer if
        value is negative. If state of filling does not change within delay
        time, stirrer is stopped and error message is prompted.
        """
        if not GPIO.input(stirrer_pin):
            self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 102)
            self.root.mixer_first_run_flag = True
        else:
            self.driver_interface_oc05.setServoPosition(self.ports["mixer"], 180)

            if self.root.mixer_first_run_flag:
                self.root.mixer_first_run_flag = False
                self.root.start_time = time.time()

            if time.time() - self.root.start_time > self.error_delay:
                self.stop_motors()
                tk.messagebox.showwarning(
                    "Check ball reservoir",
                    (
                        "There is no new ball detected for several seconds. "
                        "Please check ball reservoir! "
                        "And then restart programm!"
                    ),
                )
                time.sleep(2)
                self.root.mixer_first_run_flag = True

        self.root.after(self.checkup_delay, self.sensor_loop)


def run_gui():
    # initialisation XinaBox OC05
    OC05 = xOC05()
    OC05.init(50)
    OC03 = xOC03()
    OC03.init()

    # specify driver ports
    ports = {}
    ports["servo_horizontal"] = 1
    ports["servo_vertical"] = 2
    ports["motor_top_right"] = 3
    ports["motor_top_left"] = 6
    ports["motor_bottom_center"] = 7
    ports["servo_ball_feeder"] = 8
    ports["mixer"] = 5

    # initialize servo positions
    OC05.setServoPosition(ports["servo_horizontal"], 30)
    OC05.setServoPosition(ports["servo_vertical"], 30)
    OC05.setServoPosition(ports["motor_top_right"], 30)
    OC05.setServoPosition(ports["motor_top_left"], 30)
    OC05.setServoPosition(ports["motor_bottom_center"], 30)
    OC05.setServoPosition(ports["servo_ball_feeder"], 30)
    OC05.setServoPosition(ports["mixer"], 102)
    OC03.writePin(True)
    time.sleep(1)

    # specify GPIO Ports
    stirrer_port = 21

    # initialize GPIO ports
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(stirrer_port, GPIO.IN)

    # initialize Tkinter
    root = tk.Tk()
    BallLauncherGUI(root, ports, OC05, OC03)

    # GUI main loop
    root.mainloop()

    # cleanup
    GPIO.cleanup()


if __name__ == "__main__":
    run_gui()

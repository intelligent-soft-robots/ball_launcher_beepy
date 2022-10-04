# ---------------------------------------------------------------
import time

from tkinter import *
from tkinter import messagebox

from RPi import GPIO
from xOC05 import xOC05
from xOC03 import xOC03


# Initialisierung XinaBox OC 05
OC05 = xOC05()
OC05.init(50)
OC03 = xOC03()
OC03.init()

# Portbestimmung
servo_horizontal = 1
servo_vertical = 2
motor_top_right = 3
motor_top_left = 6
motor_bottom_center = 7
servo_ball_feeder = 8
mixer = 5

# GPIO Ports
ball_queue_sensor_pin = 21

# Ports initialisierung
OC05.setServoPosition(servo_horizontal, 30)
OC05.setServoPosition(servo_vertical, 30)
OC05.setServoPosition(motor_top_right, 30)
OC05.setServoPosition(motor_top_left, 30)
OC05.setServoPosition(motor_bottom_center, 30)
OC05.setServoPosition(servo_ball_feeder, 30)
OC05.setServoPosition(mixer, 102)
OC03.writePin(True)
time.sleep(1)

# Initialisierung GPIO Ports
GPIO.setmode(GPIO.BCM)
GPIO.setup(ball_queue_sensor_pin, GPIO.IN)

# Wert fuer Ballzufuehrung Servo
ball_feeder_endposition = 180

# Parameter Mixer
checkup_delay = 2000  # [ms]
error_delay = 10.0  # [s]

# Tkinter
root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (800, 400))
root.config(bg="grey")

root.start_time = time.time()
root.mixer_first_run_flag = True


class SliderMotor:
    def __init__(self, title, X, Y, AUSGANG, gain):
        def motor_soll(val):
            motor_speed = int(val)
            motor_speed += gain
            print(f"Turning speed {title}: {motor_speed}")
            OC05.setServoPosition(AUSGANG, motor_speed)

        self.slider = Scale(
            root,
            from_=150,
            to=30,
            orient=VERTICAL,
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

        self.title = Label(root, text=title, font=("Arial", 14), bg="grey", fg="yellow")
        self.title.place(x=X + 10, y=Y - 25)


class SliderServoVertical:
    def __init__(self, title, X, Y, AUSGANG):
        def servo_vertical_soll(val):
            serpos = int(val)
            print(f"Servo vertical: {serpos}")
            OC05.setServoPosition(AUSGANG, serpos)
            # time.sleep(2)

        self.slider = Scale(
            root,
            from_=150,
            to=30,
            orient=VERTICAL,
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

        self.title = Label(root, text=title, font=("Arial", 12), bg="grey", fg="green")
        self.title.place(x=X + 10, y=Y - 25)


class SliderServoHorizontal:
    def __init__(self, title, X, Y, AUSGANG):
        def servo_horizontal_soll(val):
            serpos = int(val)
            print(f"Servo horizontal: {serpos}")
            OC05.setServoPosition(AUSGANG, serpos)
            # time.sleep(0.1)

        self.slider = Scale(
            root,
            from_=30,
            to=150,
            orient=HORIZONTAL,
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

        self.title = Label(root, text=title, font=("Arial", 12), bg="grey", fg="blue")
        self.title.place(x=X + 10, y=Y - 25)


slider_motor_top_right = SliderMotor("Motor O R", 360, 25, motor_top_right, 0)
slider_motor_top_left = SliderMotor("Motor O L", 150, 25, motor_top_left, 0)
slider_motor_bottom_center = SliderMotor("Motor U", 255, 25, motor_bottom_center, 0)
slider_servo_phi = SliderServoHorizontal("Servo Horizontal", 0, 300, servo_horizontal)
slider_servo_theta = SliderServoVertical("Up/Down", 0, 25, servo_vertical)

# ***** Programm beenden *****
def stop_motors():
    OC05.setServoPosition(motor_top_right, 30)
    OC05.setServoPosition(motor_top_left, 30)
    OC05.setServoPosition(motor_bottom_center, 30)
    OC05.setServoPosition(mixer, 102)  # Nullposition Servo


def close():
    stop_motors()

    OC03.writePin(False)
    time.sleep(0.2)
    root.destroy()


btn_close = Button(
    root, bd=4, bg="#D6992F", text="EXIT", font=("Arial", 20, "bold"), command=close
)
btn_close.place(x=510, y=310, width=250, height=80)

# ***** Ball schiessen *****
def shot_ball():
    OC05.setServoPosition(servo_ball_feeder, 30)
    OC05.setServoPosition(mixer, 180)
    time.sleep(0.5)  # default 0.5
    servo_gain = 0
    while servo_gain <= ball_feeder_endposition:
        servo_gain += 1.5
        OC05.setServoPosition(servo_ball_feeder, servo_gain)
    else:
        OC05.setServoPosition(servo_ball_feeder, 30)
        OC05.setServoPosition(mixer, 102)


btn_single_shot = Button(
    root,
    bd=4,
    bg="#0CC3F8",
    text="SINGLE SHOT",
    font=("Arial", 18, "bold"),
    command=shot_ball,
)
btn_single_shot.place(x=510, y=30, width=250, height=120)

# ***** Multischuss *****
def add_ball():
    value = int(lb_n_balls["text"])
    lb_n_balls["text"] = f"{value + 1}"
    multi_ball = value + 1
    print(f"+1 Multi Ball: {multi_ball}")


def add_multiple_balls():
    value = int(lb_n_balls["text"])
    lb_n_balls["text"] = f"{value + 10}"
    multi_ball = value + 10
    print(f"+10 Multi Ball: {multi_ball}")


def remove_ball():
    value = int(lb_n_balls["text"])
    if value != 0:
        lb_n_balls["text"] = f"{value - 1}"
        multi_ball = value - 1
        print(f"-1 Multi Ball: {multi_ball}")


def remove_multiple_balls():
    value = int(lb_n_balls["text"])
    if value >= 10:
        lb_n_balls["text"] = f"{value - 10}"
        multi_ball = value - 10
        print(f"-10 Multi Ball: {multi_ball}")


def multiple_balls():
    counter = int(lb_n_balls["text"])
    print(f"Multi Ball Counter: {counter}")
    while counter != 0:
        counter = counter - 1
        OC05.setServoPosition(servo_ball_feeder, 30)
        OC05.setServoPosition(mixer, 180)
        time.sleep(0.5)
        servo_gain = 0
        while servo_gain <= ball_feeder_endposition:
            servo_gain += 0.5
            OC05.setServoPosition(servo_ball_feeder, servo_gain)
        else:
            OC05.setServoPosition(servo_ball_feeder, 30)
            OC05.setServoPosition(mixer, 102)


btn_shoot = Button(
    root,
    bd=4,
    bg="#00FF99",
    text="Multiball",
    font=("Arial", 14, "bold"),
    command=multiple_balls,
)
btn_shoot.place(x=510, y=170, width=120, height=120)

btn_add_ball = Button(
    root, bd=4, bg="#00FF00", text="+1", font=("Arial", 10, "bold"), command=add_ball
)
btn_add_ball.place(x=630, y=170, width=60, height=40)
btn_add_multiple_balls = Button(
    root,
    bd=4,
    bg="#AAFF00",
    text="+10",
    font=("Arial", 10, "bold"),
    command=add_multiple_balls,
)
btn_add_multiple_balls.place(x=690, y=170, width=60, height=40)
btn_remove_ball = Button(
    root,
    bd=4,
    bg="#006600",
    text="-1",
    font=("Arial", 10, "bold"),
    command=remove_ball,
)
btn_remove_ball.place(x=630, y=250, width=60, height=40)
btn_remove_multiple_balls = Button(
    root,
    bd=4,
    bg="#666600",
    text="-10",
    font=("Arial", 10, "bold"),
    command=remove_multiple_balls,
)
btn_remove_multiple_balls.place(x=690, y=250, width=60, height=40)

lb_n_balls = Label(root, bd=4, bg="#009900", font=("Arial", 10, "bold"), text="0")
lb_n_balls.place(x=630, y=210, width=120, height=40)


# ***** Sensorloop *****
def sensor_loop():
    if not GPIO.input(ball_queue_sensor_pin):
        OC05.setServoPosition(mixer, 102)
        root.mixer_first_run_flag = True
    else:
        OC05.setServoPosition(mixer, 180)

        if root.mixer_first_run_flag:
            root.mixer_first_run_flag = False
            root.start_time = time.time()

        if time.time() - root.start_time > error_delay:
            stop_motors()
            messagebox.showwarning(
                "Check ball reservoir",
                (
                    "There is no new ball detected for several seconds. "
                    "Please check ball reservoir! "
                    "And then restart programm!"
                ),
            )
            time.sleep(2)
            root.mixer_first_run_flag = True

    root.after(checkup_delay, sensor_loop)


root.after(checkup_delay, sensor_loop)

# ***** Eingabenende *****
root.mainloop()

# ***** Cleanup *****
GPIO.cleanup()

# ---------------------------------------------------------------

import time
import tkinter as tk


class BallLauncherGUI:
    def __init__(self, root, demo_mode: bool) -> None:
        self.root = root

        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (800, 400))
        self.root.config(bg="grey")

        self.root.start_time = time.time()
        self.root.mixer_first_run_flag = True

        # control parameters
        self.checkup_delay = 2000  # [ms]
        self.launch_counter = 0

        self.demo_mode = demo_mode

        # Hardware interface
        if not self.demo_mode:
            from .ball_launcher_control import BallLauncherControl

            self.launcher = BallLauncherControl()

        self.phi = 0.5
        self.theta = 0.5
        self.top_left_motor = 0.0
        self.top_right_motor = 0.0
        self.bottom_motor = 0.0

        ## GUI elements
        self.place_slider(170, 25, "Motor TL", "#CF5369", self.set_motor_top_left)
        self.place_slider(285, 25, "Motor BC", "#CF5369", self.set_motor_bottom_center)
        self.place_slider(400, 25, "Motor TR", "#CF5369", self.set_motor_top_right)

        self.place_slider(20, 300, "Left/Right", "#006c66", self.set_phi, vertical=True)
        self.place_slider(20, 25, "Up/Down", "#ffba4d", self.set_theta)

        self.place_button(
            530, 170, 120, 120, "#00FF99", "Launch\nCounter", 14, self.launch_multi
        )
        self.place_button(650, 170, 60, 40, "#00FF00", "+1", 10, self.add_ball)
        self.place_button(710, 170, 60, 40, "#AAFF00", "+10", 10, self.add_10_balls)
        self.place_button(650, 250, 60, 40, "#006600", "-1", 10, self.remove_ball)
        self.place_button(710, 250, 60, 40, "#666600", "-10", 10, self.remove_10_balls)
        self.place_button(530, 310, 240, 80, "#D6992F", "EXIT", 20, self.close)
        self.place_button(530, 30, 240, 120, "#0CC3F8", "LAUNCH", 18, self.launch_ball)

        # Tkinter label for ball counter display
        self.lb_n_balls = tk.Label(
            self.root, bd=4, bg="#009900", font=("Arial", 10, "bold"), text="0"
        )
        self.lb_n_balls.place(x=650, y=210, width=120, height=40)

        # run sensor loop
        self.root.after(self.checkup_delay, self.sensor_loop)

    def place_slider(self, x, y, name, color, command, vertical=False):
        default_value = 50

        if vertical:
            orient = tk.HORIZONTAL
            length = 455
            min_value = 100.0
            max_value = 0.0
        else:
            orient = tk.VERTICAL
            length = 200
            min_value = 0.0
            max_value = 100.0

        self.delta_value = abs(max_value - min_value)

        if "Motor" in name:
            default_value = 0

        slider = tk.Scale(
            self.root,
            from_=max_value,
            to=min_value,
            orient=orient,
            length=length,
            width=50,
            bg="grey",
            bd=5,
            font=("Arial", 16),
            fg=color,
            sliderlength=50,
            troughcolor=color,
            command=command,
        )
        slider.set(default_value)
        slider.place(x=x, y=y)

        slider_label = tk.Label(
            self.root, text=name, font=("Arial", 14), bg="grey", fg=color
        )
        slider_label.place(x=x, y=y, anchor="sw")

    def place_button(self, x, y, width, height, color, text, size, command):
        button = tk.Button(
            self.root,
            bd=4,
            bg=color,
            text=text,
            font=("Arial", size, "bold"),
            command=command,
        )
        button.place(x=x, y=y, width=width, height=height)

    def set_phi(self, value):
        self.phi = float(value) / self.delta_value
        self.set_current_state()

    def set_theta(self, value):
        self.theta = float(value) / self.delta_value
        self.set_current_state()

    def set_motor_top_left(self, value):
        self.top_left_motor = float(value) / self.delta_value
        self.set_current_state()

    def set_motor_top_right(self, value):
        self.top_right_motor = float(value) / self.delta_value
        self.set_current_state()

    def set_motor_bottom_center(self, value):
        self.bottom_motor = float(value) / self.delta_value
        self.set_current_state()

    def set_current_state(self):
        if not self.demo_mode:
            self.launcher.set_state(
                phi=self.phi,
                theta=self.theta,
                top_left_motor=self.top_left_motor,
                top_right_motor=self.top_right_motor,
                bottom_motor=self.bottom_motor,
            )

    # launching interface
    def launch_ball(self):
        """Launches ball with parameters set via sliders."""
        if not self.demo_mode:
            self.launcher.launch_ball()

    def add_ball(self):
        """Increments multi-shot counter by 1."""
        self.launch_counter += 1
        self.update_ball_label()

    def add_10_balls(self):
        """Increments multi-shot counter by 10."""
        self.launch_counter += 10
        self.update_ball_label()

    def remove_ball(self):
        """Decrements multi-shot counter by 1."""
        if self.launch_counter >= 1:
            self.launch_counter -= 1
        self.update_ball_label()

    def remove_10_balls(self):
        """Decrements multi-shot counter by 10."""
        if self.launch_counter >= 10:
            self.launch_counter -= 10
        else:
            self.launch_counter = 0
        self.update_ball_label()

    def launch_multi(self):
        """Launches number of balls specified in multi-shot counter."""
        while self.launch_counter > 0:
            self.launch_counter -= 1
            self.launch_ball()

            self.update_ball_label()

            time.sleep(4)

    def update_ball_label(self):
        self.lb_n_balls["text"] = str(self.launch_counter)

    def sensor_loop(self):
        """Checks state of filling sensor and activates reservoir stirrer if
        value is negative. If state of filling does not change within delay
        time, stirrer is stopped and error message is prompted.
        """
        if not self.demo_mode:
            self.launcher.check_ball_supply()
        self.root.after(self.checkup_delay, self.sensor_loop)

    def close(self):
        """Stop motors after exiting program"""
        if not self.demo_mode:
            self.launcher.set_state(0.5, 0.5, 0.0, 0.0, 0.0)

        time.sleep(1.0)
        self.root.destroy()

    def __exit__(self):
        self.close()


def run_gui(demo_mode: bool = False):
    root = tk.Tk()
    BallLauncherGUI(root, demo_mode)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

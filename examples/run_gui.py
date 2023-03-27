from python.ball_launcher_beepy.ball_launcher_gui import run_gui


def run_demo_mode():
    run_gui(demo_mode=True)


def run_gui_directly():
    run_gui()


if __name__ == "__main__":
    run_gui_directly()

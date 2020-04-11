from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['ball_launcher_beepy'],
    package_dir={'ball_launcher_beepy': 'python/ball_launcher_beepy'},
)

setup(**d)

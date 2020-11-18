from distutils.core import setup

setup(
    name="ball_launcher_beepy",
    version="0.5",
    author="Nico Gürtler",
    packages=["ball_launcher"],
    install_requires=["pyzmq", "protobuf"]
)

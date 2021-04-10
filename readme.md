# Ball Launcher
Ball launcher control (Python), server (Python) and clients (Python or C++) that enable remote control of the ball launcher.

## Installation
Installation under Ubuntu 16.04 or Ubuntu 18.04

### Requirements
* libzmq (ZeroMQ)
* protobuf (Protocol buffers)

The server side additionally needs
* xinabox-OC03
* xinabox-OC05

```bash
sudo apt install libzmq3-dev
sudo apt install protobuf-compiler libprotobuf-dev

# for server side only (TODO: Does this need a sudo?)
pip3 install xinabox-OC05
pip3 install xinabox-OC03
```

### Build using CMake
In build directory:

```bash
cmake path/to/repository
make install
```

This will generate the ball_launcher_pb2.py file in the ball_launcher subdirectory of the repository. In the repository directory:

```bash
pip install --editable .
```

### Configuration file

The off ticks of the PWM signals as well as sleep times can be adjusted in a JSON file at `~/.ball_launcher_config.json". Note: The comments were inserted for clarification but are not supported by JSON. Do not add them to the actual file.

```json
{
    # channels used in servo driver
    "channels": {
      "phi": 1, # azimuthal angle of launcher
      "theta": 2, # altitude of launcher
      "motor_top_left": 6, # motor of top left wheel
      "motor_top_right": 3, # motor of top right wheel
      "motor_bottom": 7, # motor of bottom wheel
      "ball_supply": 8, # pushes ball towards wheels
      "stirrer": 5 # stirs ball in funnel
    },
    # max and min values for "off" tick value of pulse
    "ticks":
    {
      "phi": [30, 150],
      "theta": [30, 150],
      "motor": [30, 150], 
      "motor_top_left_offset": [0, 0], # offset is added to min/max respectively
      "motor_top_right_offset": [0, 0],
      "motor_bottom_offset": [10, 10],
      "ball_supply_push": [30, 180],
      "stirrer": [102, 180]
    },
    "times": {
      # time to sleep after changing PWM signal in order to give system time
      # to reach a stationary configuration. TODO: Adjust if necessary
      "t_sleep": 1.0,
      # time for the ball to fall to bottom of pipe in seconds
      "t_ball_fall": 0.5
    }
}
```

## Usage

### Start server
On Raspberry Pi built into ball launcher (in repository directory),

```bash
python tests/run_server.py port_number
```
where port\_number specifies the port number, e.g., 5555.

### Creating a client in Python and launching a ball
See tests/launch\_ball\_from\_client.py

```python
import sys

import ball_launcher.ball_launcher_client as ball_launcher_client

ip_address = sys.argv[1]
port = int(sys.argv[2])
client = ball_launcher_client.BallLauncherClient(ip_address, port)

client.set_state(
        phi = 0.5, 
        theta = 0.5, 
        top_ang_vel = 0.3, 
        bottom_ang_vel = 0.4)

client.launch_ball()
```

### Creating a client in C++ and launching a ball
See tests/launch\_ball.cpp

```cpp
#include <iostream>
#include <string>

#include "ball_launcher_client.h"

using namespace std;

int main(int argc, char* argv[]){
    BallLauncherClient bl_client(string(argv[1]), stoi(argv[2]));

    bl_client.set_state(0.5, 0.5, 0.5, 0.5);
    bl_client.launch_ball();

    return 0;
}
```

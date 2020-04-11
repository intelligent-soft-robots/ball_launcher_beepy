# Ball Launcher
Ball launcher control (Python), server (Python) and clients (Python or C++) that enable remote control of the ball launcher.

## Installation
Installation under Ubuntu 16.04 or Ubuntu 18.04

### Requirements
* libzmq (ZeroMQ)
* protobuf (Protocol buffers)

The server side additionally needs
* Adafruit\_PCA9685

```bash
sudo apt install libzmq3-dev
sudo apt install protobuf-compiler libprotobuf-dev
sudo pip install pyzmq

# for server side only
sudo pip install adafruit-pca9685
```

### Build using CMake
In build directory
```bash
cmake path/to/repository
make
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

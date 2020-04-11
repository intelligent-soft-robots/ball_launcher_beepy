#include <iostream>
#include <string>

#include "ball_launcher_beepy/ball_launcher_client.hpp"

using namespace std;

int main(int argc, char* argv[]){
    if(argc == 3){
        BallLauncherClient bl_client(string(argv[1]), stoi(argv[2]));

        bl_client.set_state(0.5, 0.5, 0.5, 0.5);
        bl_client.launch_ball();

    }
    else{
        cout << "Usage: launch_ball ip_address port_number" << endl;
    }
    return 0;
}

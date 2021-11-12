#include <zmq.hpp>
#include <string>

#include "ball_launcher.pb.h"

/// Ball launcher client, provides methods for setting the state and for launching a ball remotely.
/** Uses ZMQ for communication with ball launcher server.
 */
class BallLauncherClient{
    private:
        void* context;
        void* requester;
    public:
        /// Constructor expects string containing ip address of ball launcher server and port number.
        BallLauncherClient(const std::string& ip_address, const int port_number);

        ~BallLauncherClient();

        /// Set state, i.e., orientation of launcher and angular velocities of spinning wheels.
        /**
         * @param phi Azimuthal angle of launcher (in [0, 1])
         * @theta theta altitude of launcher (in [0, 1])
         * @top_left_motor activation of top left motor (in [0, 1], default 0.0)
         * @top_right_motor activation of top right motor (in [0, 1], default 0.0)
         * @bottom_motor activation of bottom motor (in [0, 1], default 0.0)
         */
        bool set_state(const double phi, const double theta, const double top_left_motor, 
                       const double top_right_motor, const double bottom_motor);

        
        /// Launch single ball
        bool launch_ball();
};

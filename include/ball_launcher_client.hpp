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
         * @top_ang_vel top_ang_vel angular velocity of upper wheel (in [0, 1])
         * @bottom_ang_vel bottom_ang_vel angular velocity of lower wheel (in [0, 1])
         */
        bool set_state(const double phi, const double theta, const double top_ang_vel, const double bottom_ang_vel);

        
        /// Launch single ball
        bool launch_ball();
};

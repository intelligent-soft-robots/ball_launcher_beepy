#include "ball_launcher_client.hpp"

using namespace std;

BallLauncherClient::BallLauncherClient(const string& ip_address, const int port_number){
    context = zmq_ctx_new();
    requester = zmq_socket(context, ZMQ_REQ);
    zmq_connect(requester, (string("tcp://") + ip_address + ":" + to_string(port_number)).data());
}

BallLauncherClient::~BallLauncherClient(){
    zmq_close(requester);
    zmq_ctx_destroy(context);
}

bool BallLauncherClient::set_state(const double phi, const double theta, const double top_ang_vel, const double bottom_ang_vel){
    ball_launcher::Request request;

    request.set_request(ball_launcher::Request::SET_STATE);
    ball_launcher::Request_State* state = new ball_launcher::Request_State;// = request.state();
    state->set_phi(phi);
    state->set_theta(theta);
    state->set_top_ang_vel(top_ang_vel);
    state->set_bottom_ang_vel(bottom_ang_vel);
    request.set_allocated_state(state);

    string msg_string; 
    request.SerializeToString(&msg_string);


    zmq_send(requester, msg_string.data(), msg_string.size(), 0);

    char reply_buffer[16];
    zmq_recv(requester, reply_buffer, 16, 0);
    string reply_string(reply_buffer);

    if(reply_string.size()){
        if(reply_string == "1")return true;
        else return false;
    }
    else{
        return false;
    }
}

bool BallLauncherClient::launch_ball(){
    ball_launcher::Request request;

    request.set_request(ball_launcher::Request::LAUNCH_BALL);
    string msg_string; 
    request.SerializeToString(&msg_string);

    zmq_send(requester, msg_string.data(), msg_string.size(), 0);

    char reply_buffer[16];
    zmq_recv(requester, reply_buffer, 16, 0);
    string reply_string(reply_buffer);

    if(reply_string.size()){
        if(reply_string == "1")return true;
        else return false;
    }
    else{
        return false;
    }
}

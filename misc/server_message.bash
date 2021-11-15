# for copying / paste in the 
# file /home/pi/.bashrc of 
# the ball launcher raspberry pi

echo "-----------------------------------"
echo "| Welcome to ball launcher beepy  |"
echo "-----------------------------------"
echo ""
echo "to ssh to me: user pi, password: ball"
echo ""
echo "- sourcing colcon workspace"
source /home/pi/Workspaces/ball_launcher/workspace/install/setup.bash
echo "- killing already running server"
pid=$(ps aux | grep ball_launcher_server | grep -v grep | awk '{print $2}')
if [ ! -z "$pid" ]; then
    kill ${pid}
fi
ip=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
echo "- starting the ball launcher server on IP ${ip} and PORT 5555"
ball_launcher_server 
 
 

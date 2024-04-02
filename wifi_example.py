from XRPLib.defaults import *
from wifi import *
import time

ssid = 'ServerTest' #Replace with your AP's name
passkey = 'robottest' #Replace with your AP's password
ip = '192.168.4.30' #Replace with desired ip address, usually in the form 192.168.4.*** replacing *** with your desired number.


#########
# NOTES #
#########

# Closing the remote session will restart your robot's wifi module requiring a full restart.
# Fully power down robot before starting program after running off battery
# Default port is 50000



#####################
# EXAMPLE FUNCTIONS #
#####################

# The following are example functions that can be run as called from the remote terminal.
# These functions can be modified, appended etc so long as they are passed to net.add_functions
# with the appropriate keyword. For instance, when "w" is sent from the remote terminal the function
# "forward" is called.
# The return value will be printed to the remote terminal.


def forward_fast():
    drivetrain.set_speed(100, 100)
    time.sleep(1)
    drivetrain.set_speed(0,0)
    return 'Moving Forward Fast'
    
def forward():
    drivetrain.set_effort(0.5, 0.5)
    time.sleep(.6)
    drivetrain.set_effort(0,0)
    return 'Moving Forward'
    
def right():
    drivetrain.set_effort(0.5,-0.5)
    time.sleep(.3)
    drivetrain.set_effort(0,0)
    return 'Turning Right'

def left():
    drivetrain.set_effort(-0.5,0.5)
    time.sleep(.3)
    drivetrain.set_effort(0,0)
    return 'Turning Left'

def backward():
    drivetrain.set_effort(-0.5,-0.5)
    time.sleep(.6)
    drivetrain.set_effort(0,0)
    return 'Moving Backward'

def nested():
    wireless.print(connection, 'Start')
    time.sleep(.5)
    wireless.print(connection, 'Halfway')
    time.sleep(.5)
    return 'Done'
    
funcs = {'q': forward_fast, 'w': forward, 'd': right, 'a': left, 's': backward, 'n': nested}


# To connect the robot to wifi either use a remote access point, like the university network (not Bruin-Secure, it requires credentials which aren't supported),
# or host one using the robot's own wifi module. To connect to a remote module use net.connect_to_AP(ssid, passkey, ip), then pass in the network's name "ssid",
# it's password "passkey" and the ip address you want to reach the robot at, ie: "192.168.4.42".
# If you're hosting the AP on the robot, run net.host_AP(ssid, passkey) with "ssid" being the network name you'll connect your computer to, and "passkey" again being the password.
# Since the robot will be in host mode it's IP address will automatically be 192.168.4.1

net.host_AP(ssid, passkey)

#net.connect_to_AP(ssid, passkey, ip)


# net.add_functions(funcs) will send all the functions listed in funcs over to the remote terminal, so they can be run from there.
net.add_functions(funcs)

# net.start_socket() starts the server that your computer connects to. This will block until it establishes a connection. It will return a reference to the connection which will be used later.
connection = net.start_socket() 


# The wireless.control(connection) function will place your robot in a mode where it will only respond to commands from the remote terminal, but it will do so immediately,
# if using the example functions above this will essentially be like driving an rc car. This can be used for debugging functions (or for fun :) ).

#wireless.control(connection) #Remote control

#Just like the normal print function wireless.print(connection, data) will print what you pass into the data field. The connection field is the reference you got from starting the socket.

#wireless.print(connection, data) 

#Remote control loop
while 1:
    
    wireless.control(connection)
    
    
#State machine loop
while 1:
    
    print(time.localtime())
    
    time.sleep(2)
    
    wireless.print(connection, 'Hello World!!!')
    
    wireless.print(connection, time.localtime())
    
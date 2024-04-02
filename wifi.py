from XRPLib.defaults import *
import time, network, gc
try:
    import usocket as socket
except:
    import socket



gc.enable()

if __name__ == '__main__':
    
######################
    ap = 'Test' #Replace with your AP's name
    passkey = 'test' #Replace with your AP's password
######################
   

class wireless:
    global funcs
    
    
    def control(conn): #TCP transaction
        err_cases = {'repeated': 'function found multiple times', 'none': 'no such function found'}
        req = conn.recv(1024)
        req = str(req).split("'")[1] #Clean chars received
        reqs = str(f'Request: {req}')
        print(reqs)
        #print(f'functions: {self.funcs}')
        fun = 'none' #Initialize response with None
        for func in funcs.keys(): #Looks to see if the input is one of the functions
            if func == req:
                fun = func
        #print(f'function: {fun}')
        if fun != 'none': #If func exists run it otherwise report no function
            try:
                out = funcs[fun]() 
            except Exception as e:
                out = f'Error "{e}" when running function'
        else:
            out = err_cases['none']
        try:
            conn.sendall('\n'+out+'\n') #Send response to client
        except:
            conn.send('\nerror\n')
            
    def print(conn, data):
        
        try:
            conn.sendall('\n'+str(data)+'\n')
        except:
            try:
                conn.send('\nerror\n')
            except:
                raise Exception('Critical Error')
       
            
 

class net:
    
    global funcs
    
    funcs = {}
    
    def add_functions(kwargs): #Reads functions passed from main and adds references to funcs
        for key in kwargs:
            funcs[key] = kwargs[key]
        #print(f'Recieved functions: {list(funcs.keys())}')
            
        
        
    def connect_to_AP(ssid:str=None, password:str=None, hostname:str=None):
        print(f'\nConnecting to: {ssid}, with password {password}')
        if ssid == None:
            raise RuntimeError('No ssid given')
            
        wlan = network.WLAN(network.STA_IF)
        w = network.WLAN(network.AP_IF) #Init STA mode for clean disable
        w.active(False) #Ensures STA disabled
        wlan.active(True)
        
        if hostname != None:
            wlan.config(hostname=hostname)
            print(wlan.config('hostname'))
            
        wlan.connect(ssid, password)
        max_wait = 30
        while not wlan.isconnected():
            if max_wait < 0:
                raise RuntimeError('Network connection failed')
            print('Connecting...')
            time.sleep(.4)
            max_wait -= 1
        if wlan.status() == 3: 
            print('Connected')
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )
        else:
            raise RuntimeError('Network connection failed')
        
        
    def host_AP(ssid:str='RobotServer', password:str='Password123'):
        print(f'\nHosting AP with:\nssid: {ssid}, password: {password}')
        wlan = network.WLAN(network.AP_IF)
        w = network.WLAN(network.STA_IF)
        w.active(False)
        wlan.active(0)
        wlan.config(essid=ssid, password=password, channel=1)
        wlan.active(1)
       
        
        
    def start_socket():
        
        print('Starting socket')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Initialize the socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Handles incomplete shutdowns
        sock.bind(('', 50000)) #Address, port. Keep port within available options
        sock.listen(5)

        while 1:
            
            conn, addr = sock.accept() #Conn is new socket, addr is the address communicated with
            print(f'Received connection from: {addr}')
            conn.send(f'Available functions: {', '.join(func for func in funcs.keys())}\n')
        
            return conn
                
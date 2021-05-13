import socket
import time
import cpsble

class Server:
    """
    Contains properties and actions to start a CPS server.\n
    
    To initialize a class Server :-\n
        @param host: the host name of the sever\n
        @param port: the port on the server\n
    """

    devices = []
    commands = []
    
    
    def __init__(self, host='127.0.0.1', port=6000):
        self._HOST = host
        self._PORT = port
        self.clientVehicles = []
        self.start()
    
    def start(self):
        """ Creates the Socket and listens for messages until client disconnects.\n """
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._HOST, self._PORT))
            # waits for a connection to be established
            s.listen()
            self.connection, _ = s.accept()
            with self.connection: 
                print("Server Started")    
                self.listen()                  
                     
    def listen(self):
        """ Interprets each message sent from the client to the server. """
        command = ''
        running = True
        # While there is a connection established
        while running and self.connection.fileno() != -1:
            data = self.connection.recv(1024)
            # If client sends no data
            if not data:
                break
            else:
                data = data.decode('utf-8')
                # each command is separated by ';'
                for c in data.split(';'):
                    self.commands.append(c)
                if len(self.commands) > 0:
                    
                    command = self.commands.pop(0)
                    
                    if command == 'SCAN\n':
                        self.scan() 
                    elif command == 'CONNECT\n':
                        self.connect()
                    elif command == 'DISCONNECT\n':
                        return
                    else: 
                        return
    
    def scan(self):
        """ Scan command that scans for each vehicle nearby using BLE and sends data back to the client. """
        print('---=== SCANNING FOR VEHICLES...  ===---')
        
        self.devices = cpsble.scan()
        
        # For each vehicle in the system, send the data to the client
        for device in self.devices:
            message = "SCAN;{};{};{}".format(device['address'], device['manufacturer_data'], device['localname'])
            print(message.encode("ascii", "ignore"))
            self.connection.send("{}\n".format(message).encode())
            time.sleep(0.2)

        self.connection.send("SCAN;COMPLETED\n".encode())    
        print("---=== SCANNING COMPLETE ===---")
    
    def connect(self) -> bool:
        print('---=== CONNECTING TO VEHICLES... ===---')
        if len(commands) != 2:
            self.connection.send("CONNECT;ERROR\n")
            return False
        
            
        return 0; 
    
    def disconnect(self):
        return 0 
    
if __name__ == '__main__':
    server = Server()

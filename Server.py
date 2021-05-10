import socket
import asyncio
from bleak import BleakScanner
import json
from bleak import BleakClient

commands = []

class Server:

    devices = []
    
    def __init__(self, host='127.0.0.1', port=6000):
        self._HOST = host
        self._PORT = port
        self.clientVehicles = []
        self.start()
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._HOST, self._PORT))
            s.listen()
            self.connection, _ = s.accept()
            with self.connection:
                print("Server Started")
                self.scan()
                self.listen()
                print(self.devices)
                s.close()                   
                     
    def listen(self):
        global commands
        running = True
        while running:
            data = self.connection.recv(1024)
            if not data:
                break
            else:
                data = data.decode('utf-8')
                for command in data.split(';'):
                    commands.append(command)  
                print(data)
            
    
    def act(self):
        global commands
        
        if len(commands) > 0:
            command = commands.pop(0)

            if command == 'SCAN':
                self.scan()
            elif command == 'CONNECT':
                return
            elif command == 'DISCONNECT':
                return
            else:
                return
            
    
    def scan(self):
        print('---=== SCANNING FOR VEHICLES...  ===---')
        async def discover():
            devices = await BleakScanner.discover()
            for device in devices:
                if 'Drive' in device.__str__():
                    print(device.metadata['manufacturer_data'])
                    manufacturer_data = hex(device.metadata['manufacturer_data'])
                    print(manufacturer_data)
                    address = ''
                    for addr in device.address.split('-'):
                        address = address + addr
                    self.devices.append(address.lower())

        loop = asyncio.get_event_loop()
        loop.run_until_complete(discover())
        self.connection.send("SCAN;COMPLETED\n".encode())
        print('---===   SCANNING FINISHED...    ===---')
        
    def connect(self):
        print('---=== CONNECTING TO VEHICLES... ===---')
        
        return 0; 
    
    def disconnect(self):
        return 0 
    
if __name__ == '__main__':
    server = Server()
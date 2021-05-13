import socket
import asyncio
from bleak import BleakScanner
import json
from bleak import BleakClient
import time

class Server:

    devices = []
    commands = []
    
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
                self.listen()                  
                     
    def listen(self):
        command = ''
        running = True
        while running and self.connection.fileno() != -1:
            data = self.connection.recv(1024)
            if not data:
                print("No data received")
                break
            else:
                data = data.decode('utf-8')
                for c in data.split(';'):
                    self.commands.append(c)
                if len(self.commands) > 0:
                    
                    command = self.commands.pop(0)
                    if command == 'SCAN\n':
                        self.scan() 
                        time.sleep(1)
                        self.connection.send("SCAN;COMPLETED\n".encode())
                    elif command == 'CONNECT\n':
                        self.connect()
                    elif command == 'DISCONNECT\n':
                        return
                    else: 
                        return
    
    def scan(self):
        print('---=== SCANNING FOR VEHICLES...  ===---')
        
        async def discover():
            devices = await BleakScanner.discover()
            for device in devices:
                if 'Drive' in device.__str__():
                    starting_bytes = b'\xbe\xef'
                    manufacturer_data = list(device.metadata['manufacturer_data'].values())[0]
                    starting_hex = starting_bytes.hex()
                    manufacturer_hex = manufacturer_data.hex()
                    hex_value = starting_hex + manufacturer_hex
                    hex_value = hex(int(hex_value, 16))
                    byte_array = bytearray.fromhex(hex_value[2:])
                    hex_value = bytearray.hex(byte_array)
                    print("Hex {}".format(hex_value))
                    address = ''
                    for addr in device.address.split('-'):
                        address = address + addr
                    
                    localName = "1060300120202020447269766500" if address[0] == 'e' else "1060300120202020447269766500"
                    localName_hex = hex(int(localName, 16))
                    self.devices.append({'address': address.lower(), 'manufacturer_data': hex_value, 'localname': localName_hex[2:]})
                    
        loop = asyncio.get_event_loop()
        loop.run_until_complete(discover())
        
        for device in self.devices:
            message = "SCAN;{};{};{}".format(device['address'], device['manufacturer_data'], device['localname'])
            print(message.encode("ascii", "ignore"))
            for _ in range(0, 20):
                self.connection.send("{}\n".format(message).encode())
            
            
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

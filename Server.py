import socket
import asyncio
from bleak import BleakScanner
import json
from bleak import BleakClient
import time

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
        
        async def discover():
            """ Discovers each vehicle using BLE and parses bytes into readable data for the client. """
            
            devices = await BleakScanner.discover()
            for device in devices:
                if 'Drive' in device.__str__():
                    # If the device is ANKI Drive then the starting starts contains \xbe\xef
                    starting_bytes = b'\xbe\xef'
                    starting_hex = starting_bytes.hex()
                    # Data that is specific to each vehicle 
                    manufacturer_data = list(device.metadata['manufacturer_data'].values())[0]
                    manufacturer_hex = manufacturer_data.hex()
                    
                    hex_value = starting_hex + manufacturer_hex
                    hex_value = hex(int(hex_value, 16))
                    byte_array = bytearray.fromhex(hex_value[2:])
                    hex_value = bytearray.hex(byte_array)
                    print("Hex {}".format(hex_value))
                    # Grabs Address of the vehicle
                    address = ''
                    for addr in device.address.split('-'):
                        address = address + addr
                    # Specific data needed by the client for each vehicle. 
                    localName = "1060300120202020447269766500" if address[0] == 'e' else "1060300120202020447269766500"
                    localName_hex = hex(int(localName, 16))
                    # Stores data for each vehicle in the system
                    self.devices.append({'address': address.lower(), 'manufacturer_data': hex_value, 'localname': localName_hex[2:]})
                    
        loop = asyncio.get_event_loop()
        loop.run_until_complete(discover())
        
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

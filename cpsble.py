from bleak import BleakScanner
from bleak import BleakClient
import asyncio

def scan() -> [dict]:
    """ Scan command that scans for each vehicle nearby using BLE""" 
    vehicles = []
    
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
                    vehicles.append({'address': address.lower(), 'manufacturer_data': hex_value, 'localname': localName_hex[2:]})
                    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(discover())
    
    return vehicles
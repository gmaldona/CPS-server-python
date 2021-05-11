starting_byte_data = b'\xbe\xef'
byte_data = b'\x00\x08\x08\x92R+'
print("byte_data: {}".format(byte_data))

starting_hex = starting_byte_data.hex()
byte_hex = byte_data.hex()
new_hex = starting_hex + byte_hex
print(new_hex)
print()
print()

new_hex = int(new_hex, 16)
new_hex = hex(new_hex)
print(new_hex)
barray = bytearray.fromhex(new_hex[2:])
print('byte_array: {}'.format(barray))
new_hex = bytearray.hex(barray)

print()
print("Checking against beef00080892522b")

match = True if new_hex == 'beef00080892522b' else False
print(match)

'be15beef-6186-407e-8381-0bd89c4d8df4'

byte_array = bytearray.fromhex('beef00080892522b')
print(byte_array)


"""

b'\x00\x08\x08\x92R+'

0	BE EF	1011111011101111
2	00 08	0000000000001000
4	08 92	0000100010010010
6	52 2B	0101001000101011

"""

"""
#2 -> model of the car, in this case ground shock
"""

"""
No localName. Defaulting
SCAN;1214353b5acc49948f5e2097152d59f8;beef00080892522b

No localName. Defaulting
SCAN;fedefd7b41294cc4b3bda9260265a2c3;beef0012076116e5

No localName. Defaulting
SCAN;b4cc1c1bf6d04a6b9aeba0d2269747a0;beef00090952a76c
"""

"""
beef00090952a76c
beef0012076116e5
beef00080892522b
"""
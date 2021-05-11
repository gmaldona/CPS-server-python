# CPS-server-python
A Cyber Physical System network server written in python

- Scans for BLE devices & filters for correct device       [x]
- Connects to each BLE discovered & send BLE data to client []

## Notes:
- When the server scans for BLE devices, the ANKI Vehicle will return metadata. This meta contains information about the vehicle.This information is returned in the form of json data. We want to look at the ```manufacturer-data``` data. Parsing this data will result in the client java program to decode the data and decipher the vehicle in the system. 

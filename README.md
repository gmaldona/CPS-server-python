# CPS-server-python
A Cyber Physical System network server written in python

- Scans for BLE devices & filters for correct device.       [x]
- Connects to each BLE discovered & send BLE data to client []

## Notes:
- When the server scans for BLE devices, the ANKI Vehicle will return metadata. This meta contains information about the vehicle.This information is returned in the form of json data. We want to look at the ```manufacturer-data``` data. Parsing this data will result in the client java program to decode the data and decipher the vehicle in the system. 

   -> ```\xbe\xef\x00\x08\x08\x92R+``` Tells us that the vehicle is: 
   
  | x08     |  + (2b in Hex) |
  ----------|-----------------
  | Model   |  Identifier    |
   
   <table>
      <tr>
        <th>
          x08
          </th>
        </tr>
      <tr>
        <td>
          ff
          </td>
        </tr>
    </table>
    
- Current Issues:
  - Missing two bytes of data. BE EF (\xbe\xef)

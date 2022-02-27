# CS 437 Internet of Things UIUC

## Lab 2 IoT Networking

Code and Report of Lab 2

Link for video presentation : https://uofi.box.com/s/pz7sji1m464fq45dfreanvr2spcn25lw

## Code Overview

This section is intended to provide a brief overview of the codebase. All code is well-commented, so those interested in a deeper understanding of the code should use this section to understand the high-level structure of the program, but should utilize the in-file comments for a more fine-grained understanding. 

### frontend_tutorial/bt_client.py
### frontend_tutorial/bt_server.py

Scripts to test bluetooth connectivity between Raspberry Pi and Laptop, server understamds 4 command to move the Picar "forward", "backward", "turn_left" and "turn_right". Any other command is just sent back to the client for display (echo).

### frontend_tutorial/wifi_server.py

This is used for the second part of the Lab to create a Web service, the client will receive the following information: speed, distance traveled, status (moving forward, backward, etc.) and the CPU temperature, it also executes movement command.

### electron/index.js
### electron/index.html

Front end files, displays information received from Web server about the Raspberry Pi status and send movement commands



### Luis Mariano Ovalle Castaneda (lo22)
<ul>
   
</ul>


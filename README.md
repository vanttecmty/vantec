# Vantec 
Code for autonomous boat navigation. Participating in RoboBoat 2017 edition.
Components
	imu vectornav 200
	rplidar 2
	xbees

Rplidar code file is in lib/rplidar_sdk/sdk/app/socket_transmitter/main.cpp
		executable file is in lib/rplidar_sdk/sdk/output/Linux/Release/socketTramsitter




test_path.py for comparing pathfinding version 1, 2 and 3. Version 2 is the fastest.

obtain_data.py is for saving in a file all the sensors that the boat is reading.

xbee.py sends and receives data using the xbees.


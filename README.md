DoorSensor
==========

Simple Python script that reads from the GPIO pins to see if the magnetic reed switch on the physical door to the makerspace is open or closed.  Can be used as an alarm or for the spaceAPI to show if the makerspace is open or closed.
DoorSensor.py is the actual python script that reads the door reed switch GPIO pin.
doorSensor.sh is a script made for init.d so it can be auto started at bootup.

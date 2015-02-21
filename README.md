DoorSensor
==========

## SpaceMonitor

Modular Python system to monitor a switch via a Raspberry Pi GPIO pin and
report its status via the [SpaceAPI](http://spaceapi.net/).

### Setup

The spaceMonitor.sh init script should be placed in /etc/init.d, owned by root
and group root with execute permissions.  This will ensure SpaceMonitor is
started at boot.  Values near the top of this script may need to be modified,
such as the DIR variable, if you intend to install SpaceMonitor.py in a
non-default location (see below).

The SpaceMonitor.py and SpaceMonitorTest.py scripts should, by default, be
installed in /home/pi/bin.  If you wish to install them in a different
location, you will need to modify spaceMonitor.sh, as described above.

You will also need to adjust the values in the "configuration" section near
the top of SpaceMonitor.py to point to the correct URL for your SpaceAPI
profile and to the file containing your SpaceAPI security token, which will
allow the script to update the sensor status on the SpaceAPI.

### Code overview

The main code module, SpaceMonitor.py, includes the class GPIODoorSensor,
which initializes the sensor on instantiation and provides read() and reset()
methods.  The read() method returns true if the sensor is active, meaning that
the door is closed.  The reset() method is to be called on shutdown to reset
the sensor and clean up.

Also in SpaceMonitor.py is the class SpaceAPIOpenClose, which provides
openUp() and closeUp() methods, which are called to publish the door opening
and closing events, respectively.  This class also provides a test(status)
utility method to publish an arbitrary "open", "closed" or "unknown" status,
which is used by the SpaceMonitorTest.py script for command-line access to
force the state on the SpaceAPI.

Finally, SpaceMonitor.py provides the monitor(sensor, openClose) method, which
wires instances of the two classes together, reading the sensor and publishing
its state to the SpaceAPI.

#### Testing

The SpaceMonitorTest.py module has alternate classes TestSensor and
TestOpenClose, which can stand in for GPIODoorSensor and SpaceAPIOpenClose,
respectively, for testing and troubleshooting purposes.  Run the script for a
usage summary, which includes options for various combinations of the real and
test classes.

This script also includes a utility mode which provides command-line access to
force the state on the SpaceAPI to open, closed or unknown.  This may be
useful, for example, if the sensor needs to be temporarily taken down for
maintenance and you want the SpaceAPI to accurately reflect the open/closed
state, or lack thereof.

## DoorSensor

Simple Python script that reads from the GPIO pins to see if the magnetic reed switch on the physical door to the makerspace is open or closed.  Can be used as an alarm or for the spaceAPI to show if the makerspace is open or closed.
DoorSensor.py is the actual python script that reads the door reed switch GPIO pin.
doorSensor.sh is a script made for init.d so it can be auto started at bootup.

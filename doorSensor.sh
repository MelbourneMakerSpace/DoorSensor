#! /bin/sh
# /etc/init.d/doorSensor 

### BEGIN INIT INFO
# Provides:          doorSensor
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       Script that starts the door sensor python script at startup and kills it at shutdown.
# Author:            Josh Pritt
# Creation Date:     June 29, 2014
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting door Sensor"
    # run application you want to start
    sudo python /home/pi/DoorSensor.py

    ;;
  stop)
    echo "Stopping door Sensor"
    # kill application you want to stop
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/doorSensor {start|stop}"
    exit 1
    ;;
esac

exit 0
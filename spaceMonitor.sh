#! /bin/sh
# /etc/init.d/spaceMonitor

### BEGIN INIT INFO
# Provides:          spaceMonitor
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Python script to monitor sensors at the Makerspace
# Description:       Python script to monitor door and other sensors at the Melbourne Makerspace
# Author:            Josh Pritt and Brandon Ibach
# Creation Date:     June 29, 2014
### END INIT INFO

DIR=/home/pi/bin
DAEMON=/usr/bin/python
DAEMON_NAME=spaceMonitor
DAEMON_OPTS="$DIR/SpaceMonitor.py"
DAEMON_USER=root

PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting space monitor"
    start-stop-daemon --start --quiet --pidfile $PIDFILE --make-pidfile --exec $DAEMON --background -- $DAEMON_OPTS
    log_end_msg $?
}

do_stop () {
    log_daemon_msg "Stopping space monitor"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

# Carry out specific functions when asked to by the system
case "$1" in
  start|stop)
    do_${1}
    ;;
  restart|reload|force-reload)
    do_stop
    do_start
    ;;
  status)
    status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
    ;;
  *)
    echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0

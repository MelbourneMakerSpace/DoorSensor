#!/usr/bin/env python
 
from time import sleep
import RPi.GPIO as GPIO
 
GPIO.setmode (GPIO.BOARD)
doorState = False # Set the initial door State to closed
DOOR_SENSOR = 26 # door sensor connected to GPIO physical pin
doorActive = False # State door sensor
 
GPIO.setwarnings(False)
 
GPIO.setup (DOOR_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Setup the GPIO pin connected to the door Sensor to read as input
#GPIO.setup (DOOR_SENSOR, GPIO.IN) # Setup the GPIO pin connected to the door Sensor to read as input
 
# Main program loop
while True:
 
    try:             
        # Get the current state of the sensor and store it in a variable
        doorActive = GPIO.input(DOOR_SENSOR)
        print "door Active = " + str(doorActive)
        
        if( doorActive == False ):
            #magnet is present, door is closed
            sleep(0.05)
            if(doorActive == False):
                print("Switch state FALSE, door is closed")                
        else:
            #magnet is not present, door is open
            sleep(0.05)
            if(doorActive == True):
                print("Switch state TRUE, door is open!")
            
        # Wait a while before checking again.
        sleep(1)
     
    except KeyboardInterrupt:
        GPIO.cleanup() # Clean up GPIO on CTRL+C exit
 
# End of main program loop
 
# Clean up on normal exit
GPIO.cleanup()

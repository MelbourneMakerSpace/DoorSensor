#!/usr/bin/python
# JSON TODO spacefed stream state.(open,lastchange,trigger_person,message)
#           state.icon.(open,closed) events[(name,type,timestamp,extra)]
#           contact.(phone,sip,keymasters(email alias?),irc,twitter,facebook)
#           contact.(google,identica,foursquare,email,ml,jabber)
#           contact.(issue_mail(email alias?))
#           sensors.(temperature[],door_locked[],barometer[],radiation.())
#           sensors.(humidity[],beverage_supply[],power_consumption[],wind[])
#           sensors.(network_connections[],account_balance[])
#           sensors.(total_member_count[],people_now_present[])
#           feeds.(blog,wiki,calendar,flickr).(type=rss|atom|ical,url)
#           cache.schedule=[mhd]\.[0-9]{2} projects[<string/URL>]
#           radio_show[(name,url,type=mp3|ogg,start=ISO8601,end)]
#        "ml": "melbourne-makerspace@googlegroups.com",
#curl --data-urlencode sensors='{"state":{"open":true}}' --data key=<key> https://spaceapi.net/new/space/melbourne_makerspace/sensor/set

import requests, json, logging
from sys import argv

try:
	import http.client as http_client
except ImportError:
	import httplib as http_client # Python 2
http_client.HTTPConnection.debuglevel = 1

logging.basicConfig() # Initialize logging
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

#curl --data-urlencode sensors='{"state":{"open":true}}' --data key=<token> <endpoint-url>/sensor/set
#https://spaceapi.net/new/space/melbourne_makerspace/status/json

def sendStatus(status):
	f = open("/home/pi/spaceapi-token", "r")
	key = f.readline().strip()
	r = requests.get("https://spaceapi.net/new/space/melbourne_makerspace/sensor/set", verify=False,
		params={"sensors" : json.dumps({ "state" : { "open" : status } }, separators=(',', ':')), "key" : key})
	print r.content
#	print '{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r)

def closeUp():
	sendStatus(False)
#	print "Closing up"

def openUp():
	sendStatus(True)
#	print "Opening up"

if len(argv) > 1 and argv[1] == "close":
	closeUp()
elif len(argv) > 1 and argv[1] == "open":
	openUp()
else:
	print "Usage: SpaceMonitor.py <open|close>"

#from time import sleep
#import RPi.GPIO as GPIO
# 
#GPIO.setmode (GPIO.BOARD)
#doorState = False # Set the initial door State to closed
#DOOR_SENSOR = 26 # door sensor connected to GPIO physical pin
#doorActive = False # State door sensor
# 
#GPIO.setwarnings(False)
# 
#GPIO.setup (DOOR_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Setup the GPIO pin connected to the door Sensor to read as input
##GPIO.setup (DOOR_SENSOR, GPIO.IN) # Setup the GPIO pin connected to the door Sensor to read as input
# 
## Main program loop
#while True:
# 
#    try:             
#        # Get the current state of the sensor and store it in a variable
#        doorActive = GPIO.input(DOOR_SENSOR)
#        print "door Active = " + str(doorActive)
#        
#        if( doorActive == False ):
#            #magnet is present, door is closed
#            sleep(0.05)
#            if(doorActive == False):
#                print("Switch state FALSE, door is closed")                
#        else:
#            #magnet is not present, door is open
#            sleep(0.05)
#            if(doorActive == True):
#                print("Switch state TRUE, door is open!")
#            
#        # Wait for a falling or rising edge from the door sensor before executing the code below
#        sleep(1)
#     
#    except KeyboardInterrupt:
#        GPIO.cleanup() # Clean up GPIO on CTRL+C exit
# 
## End of main program loop
# 
## Clean up on normal exit
#GPIO.cleanup()

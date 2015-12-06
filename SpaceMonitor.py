#!/usr/bin/env python
# TODO
#   Additional SpaceAPI JSON stuff we can muck with, someday...
#     spacefed stream state.(open,lastchange,trigger_person,message)
#     state.icon.(open,closed) events[(name,type,timestamp,extra)]
#     contact.(phone,sip,keymasters(email alias?),irc,twitter,facebook)
#     contact.(google,identica,foursquare,email,ml,jabber)
#     contact.(issue_mail(email alias?))
#     sensors.(temperature[],door_locked[],barometer[],radiation.())
#     sensors.(humidity[],beverage_supply[],power_consumption[],wind[])
#     sensors.(network_connections[],account_balance[])
#     sensors.(total_member_count[],people_now_present[])
#     feeds.(blog,wiki,calendar,flickr).(type=rss|atom|ical,url)
#     cache.schedule=[mhd]\.[0-9]{2} projects[<string/URL>]
#     radio_show[(name,url,type=mp3|ogg,start=ISO8601,end)]
#        "ml": "melbourne-makerspace@googlegroups.com",

class SpaceAPIOpenClose: # publish open/closed status via the SpaceAPI
	# SpaceAPI testing tools
	#   sensor (open/closed) setting                      true|false|null
	#     curl --data-urlencode sensors='{"state":{"open":true}}' --data key=<key> https://spaceapi.net/new/space/melbourne_makerspace/sensor/set
	#   status reading
	#     curl https://spaceapi.net/new/space/melbourne_makerspace/status/json
	import requests, json, logging

	# configuration
	base_uri = "https://spaceapi.net/new/space/melbourne_makerspace"
	token_file = "/home/pi/spaceapi-token" #"/home/pi/spaceapi-net.pem"

	try:
		import http.client as http_client
	except ImportError:
		import httplib as http_client # python 2

	def __init__(self):
		import warnings # spaceapi.net's SSL certificate is hosed - ignore it
		import requests.packages.urllib3.exceptions as exceptions
		warnings.simplefilter("ignore", exceptions.InsecureRequestWarning)
		#self.http_client.HTTPConnection.debuglevel = 1
		requests_log = self.logging.getLogger("requests.packages.urllib3")
		requests_log.setLevel(self.logging.INFO) #.DEBUG
		requests_log.propagate = True

	def sendStatus(self, status):
		r = ""
		f = open(self.token_file, "r")
		try:
			s = self.json.dumps({"state" : {"open" : status}}, separators=(',', ':'))
			r = self.requests.get(self.base_uri + "/sensor/set/", verify=False,
			                      params={"sensors": s, "key": f.readline().strip()})
			if self.logging.getLogger().isEnabledFor(self.logging.DEBUG):
				text = r.text
				if r.headers["content-type"] == "application/json":
					text = self.json.dumps(r.json(), sort_keys=True, indent=4,
					                       separators=(',', ': '))
				self.logging.debug('{} {}'.format(text, r))
		finally:
			f.close()
		return r

	def closeUp(self):
		self.logging.info("Closing up")
		return self.sendStatus(False)

	def openUp(self):
		self.logging.info("Opening up")
		return self.sendStatus(True)

	def test(self, arg): # utility method for setting SpaceAPI status
		if arg == "close":
			return self.closeUp().content
		elif arg == "open":
			return self.openUp().content
		elif arg == "null" or arg == "none" or arg == "na":
			self.logging.info("Resetting status to N/A")
			return self.sendStatus(None).content

class GPIODoorSensor: # read open/closed status from door sensor via GPIO
	import logging, RPi.GPIO as GPIO

	# configuration
	DOOR_SENSOR = 26 # GPIO physical pin connected to door sensor

	def __init__(self, verbose=False):
		self.verbose = verbose
		self.logging.info("Initializing GPIO Door Sensor")
		self.GPIO.setmode(self.GPIO.BOARD)
		self.GPIO.setwarnings(False)
		# setup the GPIO pin connected to the door Sensor to read as input
		self.GPIO.setup(self.DOOR_SENSOR, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
		#self.GPIO.setup(self.DOOR_SENSOR, self.GPIO.IN)

	def read(self):
		sensor = self.GPIO.input(self.DOOR_SENSOR)
		if self.verbose:
			self.logging.debug("door Active = {}".format(str(sensor)))
		return sensor

	def reset(self):
		# clean up on normal exit
		self.logging.info("Resetting GPIO Door Sensor")
		self.GPIO.cleanup()

def monitor(sensor, openClose): # loop, reading sensor and publishing status
	from time import sleep

	switchState = sensor.read() # set the initial door State to the state of the switch
	lastState = switchState
	initialCheck = True #always check the first time through when script starts!
	
	# main program loop
	try:             
		while True:
			switchState = sensor.read()
			if switchState != lastState or initialCheck:
				lastState = switchState
				initialCheck = False
				if switchState == True:
					openClose.openUp()
				else:
					openClose.closeUp()
			sleep(5)                        
			
	except KeyboardInterrupt:
		pass
	finally:
		sensor.reset() # reset sensor hardware on exit

logFormat = "%(asctime)s %(levelname)s: %(message)s"
#logDateFormat = "%m/%d/%Y %H:%M:%S"

if __name__ == "__main__":
	import logging, sys
	loglevel = logging.INFO # initialize logging
	if len(sys.argv) > 1 and sys.argv[1] == "-d":
		loglevel = logging.DEBUG
	elif len(sys.argv) > 1 and sys.argv[1] == "-q":
		loglevel = logging.WARNING
	# initialize logging
	logging.basicConfig(filename="/var/log/spacemon.log", format=logFormat,
	                    level=loglevel) #datefmt=logDateFormat,

	# start SpaceMonitor with GPIO Sensor and SpaceAPI
	monitor(GPIODoorSensor(True), SpaceAPIOpenClose())

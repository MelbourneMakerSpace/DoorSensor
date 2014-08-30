#!/usr/bin/env python
# TODO
#   Wire testing stuff into Python's unittest and/or doctest frameworks
#     Ensure, and maintain, super-easy regression testing

from SpaceMonitor import *

class TestOpenClose: # print open/closed status on the console
	def closeUp(self):
		print("Switch state TRUE, door is closed")                

	def openUp(self):
		print("Switch state FALSE, door is open!")

class TestSensor: # read open/closed status from console
	from sys import stdin

	def __init__(self):
		print "Sensor initialized"
	def read(self):
		print "Door open? ",
		return self.stdin.readline()[0].lower() != "y"
	def reset(self):
		print "Sensor reset"

if __name__ == "__main__":
	import logging # initialize logging
	logging.basicConfig(format=logFormat, level=logging.DEBUG) #, datefmt=logDateFormat
	from sys import argv
	if len(argv) < 2: # normal operating mode: console sensor and open/close
		monitor(TestSensor(), TestOpenClose())
	elif argv[1] == "-s": # real sensor, console open/close
		monitor(GPIODoorSensor(True), TestOpenClose())
	elif argv[1] == "-o": # console sensor, real open/close
		monitor(TestSensor(), SpaceAPIOpenClose())
	elif argv[1] == "-u" and len(argv) > 2: # test/utility mode for SpaceAPIOpenClose
		print SpaceAPIOpenClose().test(argv[2])
	else: # print usage instructions
		print "Usage: SpaceMonitorTest.py [ -s | -o | -u <open|close|na> ]"
		print "    Start SpaceMonitor with console sensor and open/close"
		print "         -s = Real GPIO sensor, console open/close"
		print "         -o = Console sensor, real SpaceAPI open/close"
		print "         -u = SpaceAPI open/close utility"

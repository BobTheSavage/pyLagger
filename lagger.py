#!/usr/bin/python

'''
    Will Bergen - 2013
    Simple 'lag switch' based on ipfw pipe manipulation
    Connect your system-to-lag to your box, and your box to the Internet.  Bridge the two connections.


'''

import time
import os

## Setup The Rules Method ##
def setupRules():
	print "Setting up UDP Rules..."
	os.system("ipfw add 1 pipe 1 src-port 3074")
	os.system("ipfw add 2 pipe 1 dst-port 3074")
	os.system("ipfw add 3 pipe 1 src-port 45881")
	os.system("ipfw add 4 pipe 1 dst-port 45881")
	print "Rules Set"


## Print Instruction Method ##
def printInstructions():
	print ""
	print "Available Commands:"
	print "  p    pause traffic for time t (t in ms)"
	print "  l    set local latency to 10,000ms"
	print "  z    disable all settings"
	print "  s    setup the rules (is done on load)"
	print "  i    print the help"
	print "  q    exit lagger"
	print ""

## Pause pipe for X Seconds Method ##
def pausePipe(x):
	print ""
	print "Pausing pipe for " + str(x) + " seconds..."
	killedRule = "ipfw pipe 1 config bw 0KBytes/s delay 0ms"
	os.system(killedRule)
	time.sleep(x)
	os.system(normRule)
	print "Pipe Unpaused."
	print ""

## Delete all Rules Method ##
def disableAll():
	print ""
	print "Deleting all Rules and setting Pipe to Allow Traffics..."
	os.system("ipfw delete 1")
	os.system("ipfw delete 2")
	os.system("ipfw delete 3")
	os.system("ipfw delete 4")
	print "Done."
	print ""

## Set Latency to 10kms Method ##
def setLatency(x):
	print ""
	print "Setting the Latency to 10,000ms for " + str(x) + " seconds..."
	highLatency = "ipfw pipe 1 config bw 2000KBytes/s delay 1000ms"
	os.system(highLatency)
	time.sleep(x)
	os.system(normRule)
	print "Pipe Latency Returned to 0."
	print ""

## Super Do Action Method ##
def suDo(strToRun, x):
	print ""
	print "Doing it..."
	os.system(strToRun)
	time.sleep(int(x))
	os.system(normRule)
	print "Done."
	print ""


# Setup:
quit=False;
setupRules()
normRule = "ipfw pipe 1 config bw 2000KBytes/s delay 0ms"

print ""
print "******** Manipulate an ipfw Pipe ********"
print ""
printInstructions()

# Do the Work:
while quit != True:
	var = raw_input(":")
	#print "You Selected: ", var
	if var == 'i':
		printInstructions()
	if var == 'q':
		print "Quitting..."
		exit()
	if var == 'p':
		pauseLength = int(raw_input("Pause Length (in seconds): "))
		pausePipe(pauseLength)
	if var == 'l':
		latLength = int(raw_input("Length of 10k lag: "))
		setLatency(latLength)
	if var == 'z':
		disableAll()
	if var == 's':
		setupRules()
	if var == 'speck':
		print ""
		print "Type in Exactly What You Want in 'speed,lat,dur' format."
		print "Ex: '500,300,5' would  limit the bandwidth to 500, and set latency to 300 for 5 seconds."
		print "To escape speck type 'q'.  To escape and quit lagger, type 'q!'."
		speckQuit = False
		while speckQuit != True:
			var2 = raw_input("!:")
			if var2 == 'q':
				speckQuit = True
			if var2 == 'q!':
				speckQuit = True
				quit = True
			# if grep var2 goes here - error checking
			varArray = var2.split(",")
			speed = varArray[0]
			lat = varArray[1]
			dur = varArray[2]
			runStr = "ipfw pipe 1 config bw " + speed + "KByte/s delay " + lat + "ms"
			suDo(runStr, dur)

			



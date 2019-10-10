# This is the Client (Message Sender)
# Start-up Transmitter.py and Listener.py before running this guy
import os, RPi.GPIO as GPIO, time
from socket import *
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
host = "169.254.85.68" # set to IP address of target computer
port = 1234	
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)


def doEvent(x):
	print "%i Events planned..." % x
	i = 0
	while i < x:
		data = "Xmit"
		UDPSock.sendto(data, addr)
		print ("Event: %i") % (i+1)
		GPIO.output(32, True)
		time.sleep(0.5)
		GPIO.output(32, False)
		time.sleep(0.5)
		i = i + 1
		if i == x:
			data = "Exit"
			UDPSock.sendto(data, addr)
	
	
def planEvent(x):
	i = 0
	time_ahead = 0.0025
	print "\nscheduling events\n"
	while True:
		time.sleep(2)
		high_res_future = (datetime.now().second + (datetime.now().microsecond * 10**-6)) + time_ahead
		if i == x:
			data = str(0)
			UDPSock.sendto(data, addr)
			print "All done. Executed %i scheduled events" % i
			break
		else:
			data = str(high_res_future)
			UDPSock.sendto(data, addr)
			
			GPIO.output(13, True)
			time.sleep(0.005)
			GPIO.output(13, False)
			
			while True:
				high_res_time = (datetime.now().second + (datetime.now().microsecond * 10**-6))
				if high_res_time >= high_res_future:
					GPIO.output(32, True)
					time.sleep(0.005)
					GPIO.output(32, False)
					i = i + 1
					print "Ping Yellow: %i" % i
					break

				
def getPlan():
	x = 0
	while x == 0:
		events = int(raw_input("Enter number of events you would like to invoke?\n>>> "))
		if events > 0:
			x = 1
		else:
			print "Error: must enter integer > 0\n"
	while x == 1:
		event_type = int(raw_input("Enter Event Type: Instantaneous (1) or Scheduled (2)?\n>>> ")) #i.e. Measure Ethernet Lag Jitter or Clock Jitter
		if event_type == 1:
			x = 2
		elif event_type == 2:
			x = 2
		else:
			print "Error: must enter integer: 1 or 2. Try again"
	if x == 2:
		print ("Preparing: %i type %i events\n>>> " % (events, event_type))
		return (events, event_type)
		
		
def configServer(x,y):
	data = "%i" % x
	UDPSock.sendto(data, addr)
	time.sleep(0.5)
	data = "%i" % y
	UDPSock.sendto(data, addr)
	time.sleep(0.5)
	data = raw_input("To begin, send any message to the server\n>>> ")
	UDPSock.sendto(data, addr)
	

def main():

	evts, evt_typ = getPlan()
	configServer(evt_typ, evts)
	if evt_typ == 1:
		doEvent(evts)
	elif evt_typ == 2:	
		planEvent(evts)
	print ">>> Ports Closed"
	GPIO.cleanup()
	UDPSock.close()
	os._exit(0)
	
	
if __name__ == '__main__':
	main()

# This is the Server (Message Receiver)

# For [errrno 98] address already in use do:
# ps -fA | grep python
# kill -9 "second number"

import os, RPi.GPIO as GPIO, time
from socket import *
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
host = ""
port = 1234
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)


def listenEr():
	print "Waiting to be configured..."
	i = 0
	while True:
		if i == 0:
			(data, addr) = UDPSock.recvfrom(buf)
			evt_typ = int(data)
		elif i == 1:
			(data, addr) = UDPSock.recvfrom(buf)
			evts = int(data)
			print("Configured for: %i type %i events\nWaiting for client message...") % (evts, evt_typ)
		else:
			(data, addr) = UDPSock.recvfrom(buf)
			print data
			break
		i = i + 1
	
	return (evt_typ, evts)
	
		
def doEvent(x):
	print "%i Events planned...\nWaiting to receive messages..." % x
	i = 0
	while True:
		(data, addr) = UDPSock.recvfrom(buf)
		print ("Received message %i: " + data) % (i+1)
		if data == "Xmit":
			GPIO.output(32, True)
			time.sleep(0.5)
			GPIO.output(32, False)
			time.sleep(0.5)
		elif data == "Exit":
			break
		i = i + 1
	
	
def listentoClient():
	i = 0
	print "\nlisten to client\n"
	while True:
		(data, addr) = UDPSock.recvfrom(buf)
		hi_res_future = float(data)
		
		GPIO.output(13, True)
		time.sleep(0.005)
		GPIO.output(13, False)
		
		if  hi_res_future == 0:
			print "All done. Executed %i Scheduled Events" % i
			break
		else:
			while True:
				hi_res_time = (datetime.now().second + (datetime.now().microsecond * 10**-6))
				if hi_res_time >= hi_res_future:
					GPIO.output(32, True)
					time.sleep(0.005)
					GPIO.output(32, False)
					i = i + 1
					print "Ping Blue: %i" % i
					break
	
						
		
def main():
	evt_typ, evts = listenEr()
	if evt_typ == 1:
		doEvent(evts)
	elif evt_typ == 2:
		listentoClient()
	GPIO.cleanup()
	UDPSock.close()
	os._exit(0)
		
	
if __name__=='__main__':
	main()

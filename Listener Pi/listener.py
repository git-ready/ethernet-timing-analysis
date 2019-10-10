from datetime import datetime
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
GPIO.setup(16, GPIO.IN)
GPIO.setup(22, GPIO.IN) #PPT sent
GPIO.setup(36, GPIO.IN) #PPT recieved
i = 0
j = 0
blue = 0
yellow = 0
ppt_r = 0
ppt_s = 0

#callback threads
def sentDetect(channel):
	if GPIO.input(36): 
		global ppt_s
		sec = datetime.now().second
		us =  datetime.now().microsecond * 10**-6
		ppt_s = sec + us #rising edge timestamp
	else:
		return
		
def rcvDetect(channel):
	if GPIO.input(22): 
		global ppt_r
		sec = datetime.now().second
		us =  datetime.now().microsecond * 10**-6
		ppt_r = sec + us #rising edge timestamp
	else:
		return


def blueDetect(channel):
	if GPIO.input(11): 
		global i,j,blue,yellow
		sec = datetime.now().second
		us =  datetime.now().microsecond * 10**-6
		blue = sec + us #rising edge timestamp
		i = i + 1
		print "rising edge, blue,   event: %i, timestamp (sec): %f" % (i,blue)
		if i == j: #if other has already happened
			print "\n"
			ping_delta = (blue - yellow)*1000 #convert to milliseconds
			event = i
			if int(ppt_s) == int(ppt_r) == int(yellow) == int(blue): # ensure all timestamps are for current event
				if abs(ping_delta) < 58000: # 59 seconds minus 0 seconds = 59 seconds. Integer overflow error.
					file = open("events.txt", 'a')
					file.write("%f,%i,%f,%f,%f,%f\n" % (ping_delta, event, ppt_s, ppt_r, yellow, blue))
					file.close()
		else:
			return
			

def yellowDetect(channel):
	if GPIO.input(16): 
		global i,j,blue,yellow
		sec = datetime.now().second
		us =  datetime.now().microsecond * 10**-6
		yellow = sec + us #rising edge timestamp
		j = j + 1
		print "rising edge, yellow, event: %i, timestamp (sec): %f" % (j,yellow)
		if i == j:
			print "\n"
			delta = (blue - yellow)*1000 #convert to milliseconds
			event = i
			
			if int(ppt_s) == int(ppt_r) == int(yellow) == int(blue): 
				if abs(delta) < 58000:
					file = open("events.txt", 'a')
					file.write("%f,%i,%f,%f,%f,%f\n" % (delta, event, ppt_s, ppt_r, yellow, blue))
					file.close()
		else:
			return
	
#using interrupts intead of polling
GPIO.add_event_detect(11, GPIO.BOTH, callback=blueDetect)
GPIO.add_event_detect(16, GPIO.BOTH, callback=yellowDetect)
GPIO.add_event_detect(22, GPIO.BOTH, callback=rcvDetect)
GPIO.add_event_detect(36, GPIO.BOTH, callback=sentDetect)
raw_input("listening...press any key to quit\n\n")

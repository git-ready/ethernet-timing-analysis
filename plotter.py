from matplotlib import pyplot, style, mlab
from matplotlib.pyplot import show, plot
import time
import numpy

delta = []
index = []
sent = []
elag = []
intended = []
actual = []
last_evt = 0
evt = 0
count = 0

# set graph style, turn interactive mode on to draw changes to the screen (should use draw() to refresh the plot)
pyplot.ion() 
style.use('seaborn')
# creating a figuere windows
# adding a single 1 by 1 graph (axes) to the figure
# pyplot edits these axes implicitly: you call the figure once then edit
window1 = pyplot.figure(num='Ping Offset Time Stats', figsize=[7,7], dpi=100)
graph1 = window1.add_subplot(111)																		
window2 = pyplot.figure(num='Ping Offset Time', figsize=[7,7], dpi=100)
graph2 = window2.add_subplot(111)
window3 = pyplot.figure(num='Complete Timelines', figsize=[7,7], dpi=100)
graph3 = window3.add_subplot(111)

while True:
	
	#get last index value
	with open("events.txt") as f:
		data = f.readlines()
		last = data[-1].split(",")
		last_evt = int(last[1])
		print "Checking Data..."
			
	#update if new data arrives
	if evt != last_evt:
		count = 0
		graph1.clear()
		graph2.clear()
		graph3.clear()
		evt = last_evt
		with open("events.txt") as f:
			data = f.readlines() # returns a list of all the lines from the file object
			for x in data: 
				value = x.split(',') 	   #returns a list of the strings in a single line 
				poff = float(value[0])   #1st is the ping offset (diff btwn ping times Blue-Yellow "actual-intended")
				pnum = int(value[1])	 #2nd is the ping number
				ppt_s = float(value[2])  #3rd is the 'PPT sent' time 
				ppt_r = float(value[3])  #4th is the 'PPT recvd' time
				pingY = float(value[4])  #5th is the yellow ping time
				pingB = float(value[5])  #6th is the blue ping time
				delta.append(poff)
				index.append(pnum)
				sent.append(0)
				lag = ppt_r-ppt_s #ethernet transmit lag
				planned = pingY-ppt_s  #time btwn PPT sent and intended ping time
				real = pingB-ppt_s  #time btwn PPT sent and x-mitter ping
				elag.append(0+lag*1000)
				intended.append(0+planned*1000)
				actual.append(0+real*1000)
		print "Data updated, %i points." % evt
		
		# call the graph 1 object (axes and figure), implicitly add gaussian fit
		n, bins, patches = graph1.hist(delta,bins=20,normed=1,color='steelblue',alpha=0.5,label='Ping Time Histogram\n(negative means ping is early)')
		mu = numpy.mean(delta)
		sigma = numpy.std(delta)
		y = mlab.normpdf(bins, mu, sigma)
		graph1.plot(bins, y, 'r--', linewidth=1,label='Probability Density Function')
		graph1.set_xlabel('Ping Offset Time(ms) ', fontsize=10)
		graph1.set_ylabel('Probability Density', fontsize=10)
		graph1.set_title('Ping Phase Shift Stats: $\mu$ = %f(ms), $\sigma$ = %f(ms)'%(mu,sigma), fontsize=10)
		graph1.legend(frameon=True)
		
		# call graph 2 object (axes), add scatter plot
		graph2.set_xlabel('Ping Offset Time (ms)', fontsize=10)
		graph2.set_ylabel('Event Number', fontsize=10)
		graph2.set_title('Ping Phase Shift Scatter Plot', fontsize=10)
		graph2.scatter(delta, index, s=15, marker='o',label='Single Event Time Offset')
		graph2.legend(frameon=True)
		
		# ping and message timeline plot
		graph3.set_title('Trigger and Ping Timelines', fontsize=12)
		graph3.set_xlabel('Time (ms)', fontsize=10)
		graph3.set_ylabel('Ping Number', fontsize=10)
		graph3.scatter(sent ,index, s=8, c='#1f77b4', marker='o', label='PPT Sent')
		graph3.scatter(elag ,index, s=9, c='#ff7f0e', marker='v', label='PPT Recieved')
		graph3.scatter(intended ,index, s=10, c='#2ca02c', marker='p', label='Intended Ping Time')
		graph3.scatter(actual ,index, s=11, c='#8c564b', marker='d', label='Actual Ping Time')
		graph3.legend(frameon=True)
		
		# refresh the plots
		pyplot.show(block=False)
		pyplot.pause(1)
		time.sleep(2)
			
	elif evt == last_evt:
		time.sleep(5)
		count = count + 1
		if count == 3:
			print "No new data, Exiting Loop"
			break
		
#close plots
pyplot.show(block=False)
raw_input("CLose Figures\n>>> ")	


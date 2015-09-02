#!/usr/bin/env python
import sys
import uuid
import time
import math
from threading import Thread

uid = str(uuid.uuid4())

def get_row(c):
	t = time.time()
	return (t, "%d\t%f\t%s\t%d" %(int(t), t, uid, c))

i = 0

def get_events_per_second(rate):
	events_per_second = float(rate)
	num_events_per_10_ms = events_per_second / 100.0
	return num_events_per_10_ms

num_events_per_10_ms = get_events_per_second(1000)
sys.stderr.write("num_events_per_10_ms is %f\n" %(num_events_per_10_ms))

def load_eps(file_name):
	global num_events_per_10_ms
	while True:
		try:
			f = open(file_name)
			rate = float(f.read())
			num_events_per_10_ms = get_events_per_second(rate)
			f.close()
		except:
			sys.stderr.write("Cannot read file %s\n" %(file_name))
		time.sleep(1)
	

t = Thread(target = load_eps, args = [ sys.argv[1] ])
t.daemon = True
t.start() 

cur_ts = math.floor(time.time()*100) / 100
event_this_10ms = 0
while True:
	r = get_row(i)
	t = r[0]
	t_10ms = math.floor(t * 100) / 100
	if t_10ms == cur_ts:
		if event_this_10ms >= num_events_per_10_ms:
			time_to_sleep = t_10ms +0.01 - t
			time.sleep(time_to_sleep)
	else:
		event_this_10ms = 0
		cur_ts = t_10ms
	event_this_10ms += 1
	print r[1]
	i += 1
#	time.sleep(rate)

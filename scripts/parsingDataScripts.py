import os
import sys
import datetime

def load_data_timetable(files):
# Loads timetable in the format:
# \n
# <digit|day> <3 letter code|month> <digit|year>\n
# <digit:digit|time> <text|activity>\n
# ...
# \n
# Output:
# {
# 	<class datetime|date>: [
# 		(<text|time>, <text|activity>)
# 	]
# }
	data = {}
	last_key = None
	for fName in files:
		f = open(fName,'r')
		for line in f:
			sline = line.split()
			
			if len(sline)<2:
				last_key = None
				continue
			
			if last_key is None: #new day
				if sline[1]=='Nov':
					month = 11
				elif sline[1]=='Dec':
					month = 12
				elif sline[1]=='Jan':
					month = 1
				elif sline[1]=='Feb':
					month = 2
				elif sline[1]=='Mar':
					month = 3
				elif sline[1]=='Apr':
					month = 4
				elif sline[1]=='May':
					month = 5
				elif sline[1]=='Jun':
					month = 6
				elif sline[1]=='Jul':
					month = 7
				elif sline[1]=='Aug':
					month = 8
				elif sline[1]=='Sep':
					month = 9
				else:
					print 'Cant read the month'
				dt = datetime.date(day = int(sline[0]), year = int(sline[2]), month = month)
				key = dt
				data[key] = []
				last_key = key
				continue
			
			if not last_key is None:
				data[last_key].append((sline[0],sline[1]))
				continue
		f.close()

	return data

def get_time_entry(entry):
# outputs class datetime for entry (<text|time>, <text|activity>) 
	sentry = entry[0].split(':')
	hour = int(sentry[0])
	minute = int(sentry[1])
	return datetime.time(hour = hour, minute=minute)


def get_events(files):
# Loads events in the format:
# \n
# <digit|day> <3 letter code|month> <digit|year>\n
# <text|event>\n
# ...
# \n
# Output:
# {
# 	<class datetime|date>: [
# 		<text|event>
# 	]
# }
	data = {}
	last_key = None
	for fName in files:
		f = open(fName,'r')
		for line in f:
			sline = line.split()
			
			if len(sline)<1:
				last_key = None
				continue
			
			if last_key is None: #new day
				if sline[1]=='Nov':
					month = 11
				elif sline[1]=='Dec':
					month = 12
				elif sline[1]=='Jan':
					month = 1
				elif sline[1]=='Feb':
					month = 2
				elif sline[1]=='Mar':
					month = 3
				elif sline[1]=='Apr':
					month = 4
				elif sline[1]=='May':
					month = 5
				elif sline[1]=='Jun':
					month = 6
				elif sline[1]=='Jul':
					month = 7
				elif sline[1]=='Aug':
					month = 8
				elif sline[1]=='Sep':
					month = 9
				else:
					print 'Cant read the month'
				dt = datetime.date(day = int(sline[0]), year = int(sline[2]), month = month)
				key = dt
				data[key] = []
				last_key = key
				continue
			
			if not last_key is None:
				data[last_key].append(line[:-1])
				continue
		f.close()

	return data


if __name__=='__main__':
	print get_events(['../data/events_w1.dat'])

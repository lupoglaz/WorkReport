import os
import sys
import datetime
import json
from parsingDataScripts import load_data_timetable, get_time_entry, get_events


def get_single_day_activities(day_data):
# outputs dictionary of activities during the day:
# activities_dict = {
# 	<text|activity>: class datetime.timedelta
# }
	activities_dict = {}
	for i, entry in enumerate(day_data):
		if i < (len(day_data)-1):
			t0 = get_time_entry(entry)
			t1 = get_time_entry(day_data[i+1])
			dt = datetime.timedelta(minutes = t1.minute-t0.minute, hours = t1.hour - t0.hour)
			if not entry[1] in activities_dict:
				activities_dict[entry[1]] = dt
			else:
				activities_dict[entry[1]] += dt
		else:
			break
	return activities_dict

def get_activity_time_day(data, activity):
# outputs total time of certain activity during the day:
# activity_time = {
# 	<isoformat|date> : <digit|total_hours>
# }
	activity_time = {}
	for key in sorted(data.keys()):
		activities_dict = get_single_day_activities(data[key])
		if activity in activities_dict:
			activity_time[key.isoformat()] = activities_dict[activity].total_seconds()/(60.0*60.0)
		else:
			activity_time[key.isoformat()] = datetime.timedelta(seconds=0).total_seconds()/(60.0*60.0)

	return activity_time


def get_first_and_last_activities(timings):
# outputs time of first, last activities during the day and the total time between them:
# first_and_last_time = {
#	'start': { <isoformat|date> : <isoformat|time>, ... }
#	'leave': { <isoformat|date> : <isoformat|time>, ... }
#	'total_time': { <isoformat|date> : <digit|total time>, ... }
# }
	first_and_last_time = {'start':{}, 'leave':{}, 'total_time':{}}
	for day in timings.keys():
		t0 = get_time_entry(timings[day][0])
		t1 = get_time_entry(timings[day][-1])
		dt = datetime.timedelta(minutes = t1.minute-t0.minute, hours = t1.hour - t0.hour)
		first_and_last_time['start'][day.isoformat()] = t0.hour + t0.minute/60.0
		first_and_last_time['leave'][day.isoformat()] = t1.hour + t1.minute/60.0
		first_and_last_time['total_time'][day.isoformat()] = dt.total_seconds()/(60.0*60.0)
	return first_and_last_time

def get_events_dict(events_data):
	events_dict = {}
	for day in events_data.keys():
		for i,event in enumerate(events_data[day]):
			if i==0:
				events_dict[event] = day.isoformat()
			else:
				event_string = ''
				for j in range(0,i):
					event_string+=' <br> <br>'
				event_string+=event
				events_dict[event_string] = day.isoformat()
	return events_dict


def save_dict_as_json(time_dictionary, filename):
	f = open(filename,'w')
	json.dump(time_dictionary, f, sort_keys=True)
	f.close()


if __name__=='__main__':
	data = load_data_timetable(['../data/data_w1.dat', '../data/data_w3.dat', '../data/data_w4.dat', '../data/data_w5.dat', \
		'../data/data_w6.dat', '../data/data_w7.dat', '../data/data_w8.dat', '../data/data_w9.dat', '../data/data_w10.dat', \
		'../data/data_w11.dat','../data/data_w12.dat','../data/data_w13.dat','../data/data_w14.dat','../data/data_w15.dat',\
		'../data/data_w16.dat', '../data/data_w17.dat', '../data/data_w18.dat', '../data/data_w19.dat', '../data/data_w20.dat',\
		'../data/data_w21.dat', '../data/data_w22.dat', '../data/data_w23.dat', '../data/data_w24.dat', '../data/data_w25.dat',\
		'../data/data_w26.dat', '../data/data_w27.dat'])
	events_data = get_events(['../data/events_w1.dat'])
	events_dict = get_events_dict(events_data)

	first_and_last_time = get_first_and_last_activities(data)
	first_and_last_time['events']=events_dict
	save_dict_as_json(first_and_last_time, '../json/start_leave_timings.json')
	
	code_timings = get_activity_time_day(data, 'code')
	pause_timings = get_activity_time_day(data, 'pause')
	save_dict_as_json({'code': code_timings, 
						'pause': pause_timings,
						'events': events_dict}, 
						'../json/code_pause_timings.json')







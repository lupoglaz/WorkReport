import os
import sys
import datetime
import json

def load_data_timetable(files):
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
			
	return data

def get_time_entry(entry):
	sentry = entry[0].split(':')
	hour = int(sentry[0])
	minute = int(sentry[1])
	return datetime.time(hour = hour, minute=minute)

def get_single_day_activities(day_data):
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
	activity_time = {}
	for key in sorted(data.keys()):
		activities_dict = get_single_day_activities(data[key])
		if activity in activities_dict:
			activity_time[key] = activities_dict[activity]
		else:
			activity_time[key] = datetime.timedelta(seconds=0)

	return activity_time

def save_timings_json(timings, filename):
	json_dict = {}
	for day in timings.keys():
		json_dict[day.isoformat()] = timings[day].total_seconds()/(60.0*60.0)

	f = open(filename,'w')
	json.dump(json_dict, f, sort_keys=True)
	f.close()

def save_multipletimings_json(timings_dict, filename):
	json_dict = {}
	for key in timings_dict.keys():
		json_dict[key]={}
		timings = timings_dict[key]
		for day in timings.keys():
			json_dict[key][day.isoformat()] = timings[day].total_seconds()/(60.0*60.0)

	f = open(filename,'w')
	json.dump(json_dict, f, sort_keys=True)
	f.close()


if __name__=='__main__':
	data = load_data_timetable(['../data/data_w1.dat'])

	code_timings = get_activity_time_day(data, 'code')
	#save_timings_json(code_timings, '../json/code_timings.json')

	pause_timings = get_activity_time_day(data, 'pause')
	#save_timings_json(pause_timings, '../json/pause_timings.json')
	save_multipletimings_json({'code': code_timings, 
								'pause': pause_timings}, 
								'../json/code_pause_timings.json')


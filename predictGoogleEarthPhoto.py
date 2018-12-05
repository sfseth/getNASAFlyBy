#!/usr/bin/env python3
# python 3.5.1 on Mac OS 10.9.5
# Somewhat-intelligently guess the next time a satellite photo will be taken at a position for Google Earth

import sys,requests,time,statistics,argparse

parser = argparse.ArgumentParser(description='Guess the next time a google satellite photo will be taken of a location using NASA API; can use http://www.latlong.net/ to find a specific location; Default is San Francisco.')
parser.add_argument('-lon', '--longitude', type=float, default=-122.419416, help='a floating point number representing the longitude of interest')
parser.add_argument('-lat', '--latitude', type=float, default=37.774929, help='a floating point number representing the latitude of interest')
args = parser.parse_args()
lon = args.longitude
lat = args.latitude


beginDate = '2012-01-03'
# this is predictive.. we should be able to ask for the future; TODO: add customizable dates to arguments
endDate = '2018-09-22'

def getDates(lon,lat,begin,end,apikey='9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute'): 
	# dont assume numbers are passed in as strings; sample float values above are deliberately not
	slon = str(lon) 
	slat = str(lat) 
	sbegin = str(begin) 
	rsp = requests.get('https://api.nasa.gov/planetary/earth/assets?lon=' + slon + '&lat=' + slat + '&begin=' + sbegin + '&end=' + end + '&api_key=' + apikey) 
	return rsp.json() 

def parseDates(dates):
	deltas = []
	epochTime = None
	# there's got to be a function in the time module that does this for me..
	for date in dates['results']:
		year = int(date['date'].split('-')[0])
		month = int(date['date'].split('-')[1])
		day = int(date['date'].split('-')[2].split('T')[0])
		hour = int(date['date'].split('-')[2].split('T')[1].split(':')[0])
		minute = int(date['date'].split('-')[2].split('T')[1].split(':')[1])
		second = int(date['date'].split('-')[2].split('T')[1].split(':')[2])
		# skipping first value, cant figure out a delta off of null
		if epochTime is not None:
			deltas.append(time.mktime((year,month,day,hour,minute,second, 0, 1, 0)) \
				- epochTime)
		epochTime = time.mktime((year,month,day,hour,minute,second, 0, 1, 0))
	return deltas, epochTime

def flyby(lon, lat):
	dates = getDates(lon, lat, beginDate, endDate)
	deltas, lastTime = parseDates(dates)
	next_time = lastTime + statistics.mean(deltas) + statistics.stdev(deltas)
	return next_time

if __name__=='__main__':
	print('There should be a Google/NASA satellite photo at specified location at:')
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(flyby(lon,lat))))
	

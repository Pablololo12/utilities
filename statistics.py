#!/usr/bin/env python
# Author: pabloheralm@gmail.com
#         @pablololo12

import sys
import getopt
import numpy as np
import gmplot
import os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def show_map(data):
	hr = data[:,4].astype(np.float)
	lat = np.array(data[:,0].astype(np.float))
	lon = np.array(data[:,1].astype(np.float))
	gmap = gmplot.GoogleMapPlotter(np.mean(lat), np.mean(lon), 12)
	#gmap.plot(lat, lon, 'cornflowerblue', edge_width=8)
	gmap.heatmap(lat, lon)
	gmap.draw("mymap.html")

	print("Media de pulsaciones: " + str(np.mean(hr)))

def get_statistics_dir(dire):
	data = []
	for filename in os.listdir(dire):
		data = data + get_statistics(dire+os.sep+filename)
	show_map(np.array(data))

def get_statistics_file(file):
	data = get_statistics(file)
	show_map(np.array(data))

def get_statistics(file):
	tree = ET.ElementTree(file=file)
	root = tree.getroot()
	records = []
	
	trk = root.find('{http://www.topografix.com/GPX/1/1}trk')
	trkseg = trk.find('{http://www.topografix.com/GPX/1/1}trkseg')

	for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
		latlong = trkpt.attrib
		ele = trkpt.find('{http://www.topografix.com/GPX/1/1}ele').text
		time = trkpt.find('{http://www.topografix.com/GPX/1/1}time').text
		hr = 0
		extension = trkpt.find('{http://www.topografix.com/GPX/1/1}extensions')
		if extension is not None:
			extension2 = extension.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
			hr = extension2.find('{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr').text
		records.append([float(latlong.get('lat')),float(latlong.get('lon')),float(ele),time,int(hr)])
	
	return records

def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hf:d:")
	except getopt.GetoptError:
		print("statistics.py -h | -f [file]")
		sys.exit(2)

	file = 0
	dire = 0
	for opt, arg in opts:
		if opt == '-h':
			print("-h to help")
			print("-f file")
			print("-d directory")
			sys.exit()
		elif opt == '-f':
			file = arg
		elif opt == '-d':
			dire = arg

	if file == 0 and dire == 0:
		print("Need file")
		sys.exit()

	if dire == 0:
		get_statistics_file(file)
	else:
		get_statistics_dir(dire)

if __name__ == '__main__':
    main(sys.argv[1:])
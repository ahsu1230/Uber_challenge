#!/usr/bin/python

from googlemaps import GoogleMaps

mapService = GoogleMaps()

directions1 = mapService.directions('1940 Cappelletti Ct, Mountain View, CA','Verde Tea Cafe, Villa Street, Mountain View, CA')

dist_meters = directions1['Directions']['Distance']['meters']
dist_miles = float(dist_meters / (1609.34))
dist_miles *= 100
dist_miles = int(dist_miles / 1)
dist_miles = float(dist_miles) / 100
print "meters", dist_meters
print "miles", dist_miles
for step in directions1['Directions']['Routes'][0]['Steps']:
	print step['descriptionHtml']
	
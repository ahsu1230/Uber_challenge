#!/usr/bin/python

from googlemaps import GoogleMaps, GoogleMapsError
from Queue import PriorityQueue
import string
import sys
import urllib, json, csv
import math

R_KM = 6371 # Earth's radius in km!
R_MI = 3691  # Earth's radius in miles!

# Converts Degrees to Radians (used for calculating coordinate distances)
def deg2rad(deg):
	rad = deg * math.pi/180
	return rad
	
# Least precision, but fastest (better performance), great for smaller distances
def PythagorasDistance(c1, c2, unit):
	x = (c2[1] - c1[1]) * math.cos((c1[0]+c2[0])/2)
	y = (c2[0] - c1[0])
	dist = math.hypot(x,y)
	if unit == "km":
		dist *= R_KM
	elif unit == "mi":
		dist *= R_MI
	return dist

# Truck Class with attributes & a ToString() function
class Truck:
	def __init__(self, attributeList):
		self.objectid 	= attributeList[0] # string of objectID
		self.name 		= attributeList[1]
		self.food_items 	= string.lower(attributeList[2])
		self.address 	= attributeList[3]
		self.loc_descript 	= attributeList[4]
		self.facility 		= attributeList[5]
		self.latitude 	= attributeList[6] # string latitude coordinate
		self.longitude 	= attributeList[7] # string longitude coordinate
		self.open_times	= attributeList[8]	# List of military hours
	
	def ToString(self):
		mystr = "{ " + self.objectid + ", "
		mystr += self.name + ", "
		mystr += self.food_items + ", "
		mystr += self.address + ", "
		mystr += self.loc_descript + ", "
		mystr += self.facility + ", "
		mystr += self.latitude + ", "
		mystr += self.longitude + ", "
		mystr += str(self.open_times) + " }"
		return mystr

# Priority Queue Wrapper Class (specifically for (Truck instance, distance value))
# the distance value is used as the priority
class TruckPQ (PriorityQueue):
	def __init__(self):
		PriorityQueue.__init__(self)
		self.size = 0
		return

	def put(self, item, priority):
		PriorityQueue.put(self, (priority, self.size, item))
		self.size += 1
		return

	def get(self):
		priority, _, item = PriorityQueue.get(self)
		self.size -= 1
		return item, priority

		
# Main class for managing Truck instances
class Graph:
	# Constructor and initialize attributes
	def __init__(self):
		self.TruckList = []
		self.OpenTimes = {}
		for i in range(0, 24):
			self.OpenTimes[i] = []	# New List at every Hour (assuming every day)
		self.MapService = GoogleMaps()
	
	# Initialize Graph by using the XML elements to create new Truck instances and its attributes
	def InitializeGraph(self, xml_element_List):
		for element in xml_element_List:
			newTruck = Truck(element)
			
			"""
			# If truck does not have coordinates, geocode its address
			if newTruck.address != "":
				if newTruck.address.find("SAN FRANCISCO, CA") == -1:
					newTruck.address += ", SAN FRANCISCO, CA"
				if newTruck.latitude == "" or newTruck.longitude == "":
					newLat, newLng = self.geocode( newTruck.address )
					newTruck.latitude = newLat
					newTruck.longitude = newLng
			#"""
			# For Open Times, the truck can either have "anytime" or a List of military hours
			self.ParseOpenTimes(newTruck)
			self.TruckList.append(newTruck)
		return self.TruckList
	
	"""	@func ParseOpenTimes - Add into Graph's hash to a list of trucks during a military hour
		@Parameters: A truck instance
		@Return Value:
	"""
	def ParseOpenTimes (self, truck):
		if truck.open_times == "anytime":
			for t in range(0,24):
				self.OpenTimes[t].append(truck)
		else:
			for t in truck.open_times:
				self.OpenTimes[t].append(truck)
		return
		
	"""	@func CheckTime - Checks to see if truck instance is open at a specific military hour
		@Parameters: A truck instance & the current military hour
		@Return Value: True / False
	"""
	def CheckTime(self, truck, currHour):
		if currHour == "anytime":
			return True
		return (truck in self.OpenTimes[currHour])
		
	
	"""	@func geocode - geocodes an address into coordinates (using MapService.address_to_latlng(address) doesn't work for some reason)
		@Parameters: Address String
		@Return Value: Latitude, Longitude Degree Decimal Strings
	"""
	def geocode(self, addr):
		url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
		data = urllib.urlopen(url).read()
		infoList = json.loads(data).get("results")
		if len(infoList) == 0:
			return "",""
		info = infoList[0].get("geometry").get("location")
		return info['lat'], info['lng']
		# Doesn't work for some reason...
		# lat, lng = self.MapService.address_to_latlng(address)
		# return lat, lng
	
	"""	@func CalcNearbyTrucks - Calculate List of "nearby" Trucks up until a max distance (in miles)
		- only considers & stores trucks that are "open" or have any of the specified food(s)
		- @Parameters: a Maximum Distance, current coordinates, current time, and specified foods
				current time either comes in as a List of military hours or "anytime"
				specified foods either come in as a List of food strings or "" (which means anything is ok)
		- @ReturnValue: List of "nearby" Trucks sorted by distance (from closest)
		Space Complexity: O(n) = at any one time, we will have either a pq with at most n trucks, or a list of nearby trucks (at most n)
		Time Complexity: O(nlogn) = mainly from storing truck instances into a priority queue. 
	"""
	def CalcNearbyTrucks(self, maxdist, myLat, myLng, unit, wantedFoods, currTime):
		pq = TruckPQ()
		anything = False
		foods = []
		if wantedFoods == "":	# Any food is acceptable
			anything = True
		else:
			foods = wantedFoods.split(',')
		for currTruck in self.TruckList:
			if currTruck.latitude == "" or currTruck.longitude == "":
				continue	# Truck does not have latitude or longitude, so just ignore
			try:
				lat1 = float(myLat)
				lng1 = float(myLng)
				lat2 = float(currTruck.latitude)
				lng2 = float(currTruck.longitude)
				if unit == "deg":	# need to convert to radians
					lat1 = deg2rad(lat1)
					lng1 = deg2rad(lng1)
					lat2 = deg2rad(lat2)
					lng2 = deg2rad(lng2)
				distance = PythagorasDistance( (lat1,lng1) , (lat2,lng2), "mi" )
				distance = round(distance, 2) # Round to 100th decimal point
				
				if distance < maxdist and (self.CheckTime(currTruck, currTime)):
					if not (anything):
						for f in foods:
							if currTruck.food_items.find(f) != -1:
								pq.put(currTruck, distance)
					else:
						pq.put(currTruck, distance)
			except ValueError:
				print "error!"
				continue	# problem converting to float
				
		outputList = []
		while pq.qsize() > 0:
			truck, dist = pq.get()
			outputList.append((truck,dist))
		return outputList
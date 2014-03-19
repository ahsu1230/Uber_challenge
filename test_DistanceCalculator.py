#!/usr/bin/python
# Create a matrix of vertices & edges in a grid

import math

def deg2rad(deg):
	rad = deg * math.pi/180
	return rad
		
class Coords:
	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng
		
	def Coords2Rad(self):
		self.lat = deg2rad(self.lat)
		self.lng = deg2rad(self.lng)
		
Rkm = 6371 # Earth's radius in km!

# most precision
def HaversineDistance(c1, c2):
	dLng= c2.lng - c1.lng
	dLat = c2.lat - c1.lat
	a1 = (math.sin(dLat/2))   * (math.sin(dLat/2))
	a2 = (math.sin(dLng/2)) * (math.sin(dLng/2))
	a3 = math.cos(c2.lat) * math.cos(c1.lat)
	a = a1 + a2 * a3
	c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
	dist = Rkm * c
	return dist

# Less precision, but simpler (especially for limited computational power)
def SphericalCosinesDistance(c1, c2):
	a1 = math.sin(c1.lat) * math.sin(c2.lat)
	a2 = math.cos(c1.lat) * math.cos(c2.lat)
	a3 = math.cos(c2.lng - c1.lng)
	dist = math.acos(a1 + a2 * a3) * Rkm
	return dist
	
# Least precision, but fastest (better performance), great for smaller distances
def PythagorasDistance(c1, c2):
	x = (c2.lng - c1.lng) * math.cos((c1.lat+c2.lat)/2)
	y = (c2.lat - c1.lat)
	dist = math.hypot(x,y) * Rkm
	return dist	#km!
	
# Vertex coordinates are (lat, lng)
C1 = Coords(37.7828, -122.4166)
C2 = Coords(37.7901490737255, -122.398658184604)
C1.Coords2Rad()
C2.Coords2Rad()

print "Distances in Kilometers"
print HaversineDistance(C1, C2)
print SphericalCosinesDistance(C1, C2)
print PythagorasDistance(C1, C2)
#!/usr/bin/python
# Tests the GraphHandler to make sure the Graph Nodes/Vertices/Edges/etc. are correctly made & calculated

from googlemaps import GoogleMaps
from GraphHandler import Graph

NumTotalTests = 0
NumTestsPassed = 0
def MyTest(testname, actual, expected):
	global NumTotalTests
	global NumTestsPassed
	NumTotalTests += 1
	if actual == expected:
		NumTestsPassed += 1
		print "Passed:", testname
		return True
	else:
		print "FAILED:", testname, "actual:", actual, "expected", expected
		return False
		
		
"""
	Elements are:
	0 objectid
	1 applicant name
	2 food items
	3 address
	4 location description
	5 facility type
	6 latitude
	7 longitude
	8 open times (in a list of military hours or "always")
"""
G = Graph()

addressList = [ ("Google", "1600 Amphitheatre Parkway, Mountain View, CA"),
			("Intel", "2200 Mission College Blvd, Santa Clara, CA"),
			("Castro", "500 Castro St, Mountain View, CA"),
			("88 Sushi", "506 Showers Dr, Mountain View, CA"),
			("Bangkok Bistro", "580 North Rengstorff Avenue Mountain View, CA"),
			("WhoKnows", "1760 YOSEMITE AVE")
		    ]
coordsList = []
print "Coords List:"
for AddressTuple in addressList:
	lat, lng = G.geocode(AddressTuple[1])
	#lat, lng = G.Address2Coords(AddressTuple[1])
	coordsList.append( (lat,lng) )
	print "\t", (lat, lng)

elementList = []
elementList.append(["1", addressList[0][0], "CityChicken", addressList[0][1], "", "Truck", 	  coordsList[0][0], coordsList[0][1], 	range(10,13) ])
elementList.append(["2", addressList[1][0], "citywok", addressList[1][1], "",      "Push Cart",   coordsList[1][0], coordsList[1][1], 	range(8,13) ])
elementList.append(["3", addressList[2][0], "cityBeef", addressList[2][1], "",     "Truck", 	  coordsList[2][0], coordsList[2][1], 	"anytime" ])
elementList.append(["4", addressList[3][0], "citychicken", addressList[3][1], "", "Truck", 	  coordsList[3][0], coordsList[3][1], 	[12] ])
elementList.append(["5", addressList[4][0], "Cityshrimp", addressList[4][1], "",   "Restaurant", coordsList[4][0], coordsList[4][1], 	"anytime" ])
elementList.append(["6", addressList[5][0], "citycode", addressList[5][1], "",     "Truck", 	  coordsList[5][0], coordsList[5][1], 	range(12,20) ])

# Initialize Graph... it xxpects a List of entries
TruckList = G.InitializeGraph(elementList)

	
# TESTS BEGIN! ########################################
	
# Test size of list
MAX_DIST = 5 		# in miles
MyTest("Length of TruckList", len(TruckList), 6)


myLoc = "1940 Cappelletti Ct Mountain View, CA"
myLat, myLng = G.geocode(myLoc)
print "\t", myLoc, myLat, myLng
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "", "anytime")
# List elements are in format (truck instance, distance)
for tuple in NearbyList:
	print "\t", tuple[0].name, tuple[1]

# Test if NearbyTrucks is correct
MyTest("Length of NearbyList", len(NearbyList), 4)
	
# Test if PQ ascends from minimum value to greater values
minDist = (NearbyList[0])[1]
priority = True
for i in range(1, len(NearbyList)):
	if minDist > (NearbyList[i])[1]:
		priority = False
		break
	else:
		minDist = NearbyList[i][1]
MyTest("Ascending PQ", priority, True)

# Test if PQ contains distances less than MAX_DIST
valid = True
for tuple in NearbyList:
	distance = tuple[1]
	if distance > MAX_DIST:
		valid = False
		break
MyTest("Within Max Distance", valid, True)

# Test if PQ could contain ALL nodes
NearbyList = G.CalcNearbyTrucks(100.0, myLat, myLng, "deg", "", "anytime")
MyTest("All Nodes", len(NearbyList), 6)

# Test if "chicken" is in all nearby trucks
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "chicken", "anytime")
valid = True
for tuple in NearbyList:
	truck = tuple[0]
	if truck.food_items.find("chicken") == -1:
		valid = False
		break
MyTest("Correct Foods A", valid, True)
# Test if "beef" is in all nearby trucks
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "beef", "anytime")
valid = True
for tuple in NearbyList:
	truck = tuple[0]
	if truck.food_items.find("beef") == -1:
		valid = False
		break
MyTest("Correct Foods B", valid, True)

# Test if time @ 10 hours is correct
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "", 10)
valid = True
for tuple in NearbyList:
	truck = tuple[0]
	if truck.open_times == "anytime":
		continue
	if not(10 in truck.open_times):
		valid = False
		break
MyTest("Correct Times A", valid, True)

# Test if time @ 18 hours is correct
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "", 18)
valid = True
for tuple in NearbyList:
	truck = tuple[0]
	if truck.open_times == "anytime":
		continue
	if not(18 in truck.open_times):
		valid = False
		break
MyTest("Correct Times B", valid, True)

# Test if both type of foods AND time were tested correctly
NearbyList = G.CalcNearbyTrucks(5.0, myLat, myLng, "deg", "chicken", 12)


if NumTotalTests == NumTestsPassed:
	print "***All Tests Passed!***", NumTotalTests
else:
	print "Test(s) Failed", NumTestsPassed,"/",NumTotalTests
#!/usr/bin/python
# Tests the XML Parser to make sure it correctly parsed out every entry correctly

from MyParser import XMLParser
import sys
    
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
    
    
xml_parser = XMLParser("trucks.xml")

xml_elements = ["objectid", "applicant", "fooditems", "address", "locationdescription", "facilitytype", "latitude", "longitude", "schedule"]
tagLists = xml_parser.HandleDocument("row", xml_elements)
if tagLists == XMLParser.PARSE_FAIL:
	sys.exit(XMLPARSER.PARSE_FAIL)
		
#xml_parser.PrintToTxt()

# TESTS BEGIN! ########################################

# Test size of list
MyTest("ListSize", len(tagLists), 626)

# Test first & last example by 'objectid'
MyTest("FirstExample", tagLists[0][0], "427856")
MyTest("LastExample", tagLists[len(tagLists)-1][0], "427963")

#random samples, test by 'applicant name', 'facility type', and 'latitude' & 'longitude'
MyTest("Example1a", tagLists[184][1], "The Sandwich Stand, LLC.")
MyTest("Example1b", tagLists[184][5], "Push Cart")
MyTest("Example1c",(tagLists[184][6], tagLists[184][7]), ("37.7928707497415", "-122.400747494077"))

MyTest("Example2a", tagLists[456][1], "Sun Rise Catering")
MyTest("Example2b", tagLists[456][5], "Truck")
MyTest("Example2c", (tagLists[456][6], tagLists[456][7]), ("37.790735810536", "-122.40196900168"))

print "\nTest all elements have addresses/coordinates"
c = 1
numNoAddresses = 0
numNoCoords = 0
for t in tagLists:
	if t[3] == "":
		numNoAddresses += 1
		print c, "No Address", t
	if t[6] == "" or t[7] == "":
		numNoCoords += 1
		print c, "No Coordinate"
	c += 1
print (numNoAddresses, numNoCoords)


if NumTotalTests == NumTestsPassed:
	print "***All Tests Passed!***", NumTotalTests
else:
	print "Test(s) Failed", NumTestsPassed,"/",NumTotalTests
#!/usr/bin/python

import cgi
import webapp2
import xml.dom.minidom
from MyParser import XMLParser
from GraphHandler import Graph

f = open('index.html', 'r')
INDEX_HTML = f.read()

# Preprocessing of XML File
xml_parser = XMLParser("trucks.xml")
""" 	Parse Document first by 'row'
	Then by objectID, applicant, food, address, location description, facility type, latitude, longitude
 """
xml_elements = ["objectid", "applicant", "fooditems", "address", "locationdescription", "facilitytype", "latitude", "longitude", "schedule"]
elementList = xml_parser.HandleDocument("row", xml_elements)

G = Graph()
G.InitializeGraph(elementList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write(INDEX_HTML)
		return
		
	def post(self):
		
		myLoc = cgi.escape(self.request.get('location'))
		maxDist = float(cgi.escape(self.request.get('maxdist')))
		currHour = cgi.escape(self.request.get('open'))
		wantedFood = cgi.escape(self.request.get('food'))
		
		myLat, myLng = G.geocode(myLoc)
		NearbyTrucks = G.CalcNearbyTrucks(maxDist, myLat, myLng, "deg", wantedFood, currHour)
		returnStr = str(myLat) + '|' + str(myLng) + ":::"
		for tuple in NearbyTrucks:
			truck = tuple[0]
			dist = tuple[1]
			returnStr += truck.name + '|'
			returnStr += str(dist) + ' mi' + '|'
			returnStr += truck.address + '|'
			returnStr += truck.loc_descript + '|'
			returnStr += truck.open_times + '|'
			returnStr += truck.facility+ '|'
			returnStr += truck.food_items + '|'
			returnStr += truck.latitude + '|'
			returnStr += truck.longitude + '|'
			returnStr += ":::"
		self.response.write(returnStr)
		return

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
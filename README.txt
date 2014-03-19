/////////////////// Application Information ////////////////////////
Author: Aaron Hsu
Link to Hosted Application: http://uberchallengeahsu1230.appspot.com/
Link to Hosted Repository: https://github.com/ahsu1230/Uber_Challenge/tree/master/Uber_challenge/food_trucks

File Directory:
	index.html		   - main index page of web application
	stylesheets/main.css	   - styler for main index page
	javascripts/functions.js   - main javascript functions for web application

	main.py			   - main python web server request handler
	MyParser.py		   - Handles parsing out data from XML file
	GraphHandler.py		   - Handles Truck instances & calculating distances to nearest trucks
	test_DistanceCalculator.py - Test file for calculating distances (3 ways to observe precision)
	test_xmlparser.py	   - Test file for XML parser
	test_GraphHandler.py	   - Test file for handling Truck instances & returning nearby trucks
	googlemaps.py		   - Google Maps API
	trucks.xml		   - XML file of truck data
	

/////////////////// Project Information ////////////////////////
Project 4: Food Trucks
Technical Stack: Back-end, minimal Front-end
Technical Choices: Google App Engine, Python, Google Maps API
	First time hosting a web application with Google App Engine
	First major project using Python (no prior work/course experience with Python)
	First time tinkering with Google Maps API (Javascript & Python)
	First time, in a long while, working with HTML / CSS / Javascript code

	I chose Google App Engine because it is free (doesn't require you to subscribe) 
		and it seemed very well documented & supported.
	I chose Python because it is the most familiar language supported by Google App Engine.

Algorithm (General Overview):
	Step 1: Parse truck information out of XML (Pre-processing stage)
	Step 2: Initialize List of Truck instances (Pre-processing stage)
		if any trucks do not have coordinates, geocode their address
		if trucks also do not have an address, there's not much we can do...
		very loose open time specification for trucks...

	Step 3: Retrieve user input
	Step 4: Given a coordinate (and other information), find nearby Trucks
		- To find nearby trucks, we calculate the straight line distances 
			between the current location coordinate and the coordinates of all trucks
		- Since there are only 600 trucks, brute-force calculations are very fast (and simple).
		- Place all nearby trucks into a Priority Queue to heap sort the nearest Trucks
		- Disregard trucks if they are "not open" or don't have the specified food requests
		- Time: roughly O(nlogn) Space: O(n)
	Step 5: Display list of nearby trucks back to user

Assumptions:
	- Location a user gives should be an address, but not decimal coordinates.
	- Specific foods are separated by commas. So if I wanted chicken or beef,
		I would input into the field, "chicken,beef" and all nearby trucks
		with chicken OR beef in their descriptions are returned
	- XML file
		I assume the XML file needs to be correctly formatted (no '&' or hyperlinks)
		The XML file I downloaded from the data webpage isn't correctly formatted
		so I had to either parse the hyperlinks out, replace '&' or delete some lines...

Trade-offs & Future Work:	
	- Because Google Map API functions can take a while (especially for many requests), 
		and we want to use those functions as least as possible.
		So distance is calculated through Pythagoras distances between decimal degree coordinates.

	- Look into better scaling optimizations 
		- (if we had much more trucks, would I still be able to re-use this code?)
		- If list of trucks were much more, we could use an actual Graph
		- Prepare a graph such that vertices & truck nodes lay in a grid-like fashion 
		  and perform Dijkstra's shortest path algorithm on vertices
			until the distance is greater than the max-distance or we've searched all nodes 
			(the latter is not likely to happen since there will be lots of vertices and 
			reaching the maximum distance will probably happen first)
		- for only 600-ish trucks, creating this Graph with so many vertices does not seem worth it =(

	- Have a better open-times system. 
		I left out scheduling because the truck schedules were in pdf format. Otherwise, it would
	  	be difficult to parse pdf, because the times & locations are by layout (not content).
		As of right now, only loose scheduling tests, but not really applied to the main program

		My original method would be to implement a range tree (based on Day & Hours). 
		It would take about linear space and O(logn) time to find 
		which trucks are open within a certain time frame.
		But, unfortunately, I couldn't implement that with enough time,
		so I am using a dictionary that maps a military hour to a list of open trucks
		This takes O(n) time and O(24*n) space (list of trucks open at every hour)	
		If I had more time, I would probably change the dictionary of open times
			to include different days by either using nested hashing 
				(hash[Weekday] -> hash[Hour]-> List of Trucks)
			or use a tuple (Weekday, Hour) -> List of Trucks

	- More refined front-end work
	- Better/Refined way of indexing/searching for specific foods
	- More tests because you can never have too many tests
	- Open to changes to code quality & flexibility


/////////////////// Other Cool Code ////////////////////////
Spothify - a personal remake of the online music application, Spotify.
	   Includes extensive practice with Go and distributed systems concepts
		 such as scaling, RPC, p2p, distributed consistent hashing and fault tolerance
	   Project is still in the making =)
https://github.com/ahsu1230/Spothify


/////////////////// LinkedIn Profile ////////////////////////
www.linkedin.com/pub/aaron-hsu/38/532/7b0/

(resume will be sent separately)


/////////////////// Resources ////////////////////////
https://developers.google.com/appengine/
http://www.w3schools.com/
https://developers.google.com/maps/documentation/javascript/
https://developers.google.com/maps/documentation/python/
https://developers.google.com/maps/tutorials/

http://jsfiddle.net/yV6xv/163/
http://andrew.hedges.name/experiments/haversine/
http://www.movable-type.co.uk/scripts/latlong.html
http://stackoverflow.com/questions/9289614/how-to-put-items-into-priority-queues


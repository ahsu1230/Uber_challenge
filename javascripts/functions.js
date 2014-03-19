
var map;			// Global Google Map Instance
var markers = [];
var infowindow = new google.maps.InfoWindow();

function initialize() {
        var map_canvas = document.getElementById('map_canvas');
        var map_options = {
          center: new google.maps.LatLng(37.7828, -122.4166),
          zoom: 15,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(map_canvas, map_options);
}

// Sets the map on all markers in the array.
function setAllMap(map) {
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(map);
	}
}

function makeInfoWindowEvent(map, infowindow, contentString, marker) {
	google.maps.event.addListener(marker, 'click', function() {
	    infowindow.setContent(contentString);
	    infowindow.open(map, marker);
	});
}

// Add a marker to the map and push to the array.
function addMarker(location, name) {
	var marker = new google.maps.Marker({
		position: location,
		map: map,
		title: name
	});
	makeInfoWindowEvent(map, infowindow, name, marker);
	markers.push(marker);
}

// Shows any markers currently in the array.
function showMarkers() {
	setAllMap(map);
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
	setAllMap(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
	clearMarkers();
	markers = [];
}


function generateTable(data) {	
	// Parse Data
	var ResultList = data.split(":::");
	//alert("entries: " + ResultList);
	
	// Table DOM ID
	table = document.getElementById('ResultsTable');
	var tableOutput = "";
	
	// Reset Table Rows
	var rowCount = table.rows.length;
	for (var i=rowCount-1; i>=0; i--) {
		table.deleteRow(i);
	}
	rowCount = table.rows.length;
	// Reset Map
	deleteMarkers();	
	
	var numResults = "";
	if (ResultList.length == 1) {
		numResults = "No matches found...";
		showMarkers();
		return;
	} else {
		numResults = "found ".concat(String(ResultList.length-2), " nearby trucks...");
	}
	document.getElementById('num_results').innerHTML = numResults;

	// Retrieve Current Location which is index 0 of ResultList
	myLoc = ResultList[0].split("|");
	var mylat_f = parseFloat(myLoc[0]);
	var mylng_f = parseFloat(myLoc[1]);
	
	var myloc = new google.maps.LatLng(mylat_f, mylng_f);
	var image = 'http://library.csun.edu/images/google_maps/marker-blue.png';
	var m = new google.maps.Marker({
		position: myloc,
		map: map,
		title: "My Current Location",
		icon: image
	});
	makeInfoWindowEvent(map, infowindow, "Here I am!", m);
	markers.push(m);
	map.setCenter(m.getPosition())
	
	// Add New Table Rows
	for (index=1; index < ResultList.length; index++) {
		resultRow = ResultList[index].split("|");
		if (resultRow == "" || resultRow == null) {
			continue;
		}
		var newRow = table.insertRow(rowCount);
		newRow.insertCell(0).innerHTML = resultRow[0];
		newRow.insertCell(1).innerHTML = resultRow[1];
		newRow.insertCell(2).innerHTML = resultRow[2];
		newRow.insertCell(3).innerHTML = resultRow[3];
		newRow.insertCell(4).innerHTML = resultRow[4];
		newRow.insertCell(5).innerHTML = resultRow[5];
		newRow.insertCell(6).innerHTML = resultRow[6];
		var coords = "(".concat(resultRow[7], ", ", resultRow[8], ")");
		newRow.insertCell(7).innerHTML = coords;
		table.appendChild( newRow );
		
		var lat_f = parseFloat(resultRow[7]);
		var lng_f = parseFloat(resultRow[8]);
		
		var loc = new google.maps.LatLng(lat_f, lng_f);
		addMarker(loc, resultRow[0]);
	}
	// --- Change Google Map ---
	showMarkers();
}

google.maps.event.addDomListener(window, 'load', initialize);
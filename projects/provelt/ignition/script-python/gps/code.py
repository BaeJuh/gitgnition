def inRange(lat1, lon1, lat2, lon2, radius):
	from math import sin, cos, sqrt, atan2, radians

	# approximate radius of earth in km
	R = 6373.0
	
	lat1 = radians(lat1)
	lon1 = radians(lon1)
	lat2 = radians(lat2)
	lon2 = radians(lon2)
	
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	
	distance = R * c
	distance = distance * 3280.84
	
	if distance <= radius:
		return True
	
	return False
	
def navigate(session, gpsData):
	lat1 = gpsData["latitude"].value
	lon1 = gpsData["longitude"].value
	
	dashboards = session.custom.dashboard.dashboards.gps
	for dashboard in dashboards:
		lat2 = dashboard["lat"]
		lon2 = dashboard["lon"]
		radius = dashboard["radius"]
		if gps.inRange(lat1, lon1, lat2, lon2, radius):
			session.custom.dashboard.options.gpsUrl = dashboard["url"]
			break
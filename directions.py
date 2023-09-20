import polyline
import openrouteservice
import os
from openrouteservice.directions import directions

client = openrouteservice.Client(key=os.environ['OPENROUTESERVICE_API_KEY']) 

#returns a set of points to get from start to end
def extract_coordinates_from_response(start_and_end_point):
    routes = directions(client, start_and_end_point)
    try:
        distance = routes['routes'][0]['summary']['distance']
        geometry = routes['routes'][0]['geometry']
        # Decode the polyline to get the list of coordinates
        coordinates = polyline.decode(geometry)
        return coordinates, distance
    except (KeyError, IndexError):
        return []


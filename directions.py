import polyline
import openrouteservice
from openrouteservice.directions import directions

client = openrouteservice.Client(key='5b3ce3597851110001cf6248b61898f56c394160be8a77936e312a7a') 


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


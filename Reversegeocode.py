from geopy.geocoders import Nominatim

# Initialize the geocoder (Nominatim in this example)
geolocator = Nominatim(user_agent="my_geocoder")

# Define the coordinates (latitude and longitude)


def reverse_geocode(latitude, longitude):
    # Perform reverse geocoding
    location = geolocator.reverse((latitude, longitude), language="en")
    place_name = location.address 
    return place_name
    # Extract the place name
    print("Place Name:", place_name)


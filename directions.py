from openrouteservice import deprecation
from openrouteservice.optimization import optimization, Job, Vehicle
import openrouteservice

import warnings

client = openrouteservice.Client(key='5b3ce3597851110001cf6248b61898f56c394160be8a77936e312a7a')

start_coords = (53.7974185, -1.5437941000000137)
end_coords = (53.7980618159815, -1.5029776480180885)

directions = client.directions(
    coordinates=[start_coords, end_coords],
    profile='driving-car',
    format='json'
)
print(directions)


  
from openrouteservice import deprecation
from openrouteservice.optimization import optimization, Job, Vehicle
import openrouteservice

import warnings

client = openrouteservice.Client(key='5b3ce3597851110001cf6248b61898f56c394160be8a77936e312a7a')

start_coords = (-1.540704504417448,53.806167806881845)
end_coords = (-1.5358874132664084,53.80426084639122)

directions = client.directions(
    coordinates=[start_coords, end_coords],
    profile='driving-car',
    format="WKT"
)
print(directions)


  
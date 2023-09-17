import requests
import json


driver_data = {"name": "Client1", "age": 25, "numplate": "XYZ123"}
response = requests.post("http://surveyer.pythonanywhere.com/post_driver_data", json=driver_data)
if response.status_code == 200:
    print("Client (driver) registered successfully")
    print(response)
else:
    print(f"Failed to register client. Status code: {response.status_code}")

passenger_data = {"name": "Passenger2", "age": 25}
response = requests.post("http://surveyer.pythonanywhere.com/post_passenger_data", json=passenger_data)
if response.status_code == 200:
    print("Client (passenger) registered successfully")
    print(response)
else:
    print(f"Failed to register client. Status code: {response.status_code}")

  
response = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
if response.status_code == 200:
    client_info = response.json()
    print(client_info)
else:
    print(f"Failed to get driver information. Status code: {response.status_code}")

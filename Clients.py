import requests
import json


driver_data = {"name": "Client1", "age": 25, "numplate": "XYZ123"}
response = requests.post("http://surveyer.pythonanywhere.com/receivedata", json=driver_data)
if response.status_code == 200:
    print("Client registered successfully")
else:
    print(f"Failed to register client. Status code: {response.status_code}")


passenger_name = "Client2"  
response = requests.get(f"http://surveyer.pythonanywhere.com/retrievedata{driver_data}")  
if response.status_code == 200:
    client_info = response.json()
    print(client_info)
else:
    print(f"Failed to get client information. Status code: {response.status_code}")

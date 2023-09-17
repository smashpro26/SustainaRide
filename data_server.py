import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
drivers = []
passengers = []
accepted_drivers = []

@app.route('/post_driver_data', methods=['POST'])
def Register_Driver():
    data = request.json
    drivers.append(data)
    return jsonify(drivers)

@app.route('/post_passenger_data', methods=['POST'])
def Register_Passenger():
    data = request.json
    passengers.append(data)
    return jsonify(drivers)

@app.route('/get_drivers', methods=['GET'])
def Get_Drivers():
    return jsonify(drivers)

@app.route('/get_passengers', methods=['GET'])
def Get_Passengers():
    return jsonify(passengers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
    






from flask import Flask, request, jsonify
import requests
import http
app = Flask(__name__)
drivers = []
#passengers = []



@app.route('/receivedata', methods=['POST'])
def Register_Driver():
    data = request.json 
    drivers.append(data)
    return jsonify({"message": "Driver registered successfully"})


@app.route('/retrievedata<driver_name>', methods=['GET'])
def Get_Driver(driver_name):
    for driver in drivers:
        if driver['name'] == driver_name:
            return jsonify(driver)
    return jsonify({"message" : "Driver not found"})


# Endpoint to receive data  
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json  # Get JSON data sent by Client 1
    # Process data or store it as needed
    return jsonify({"message": "Data received successfully"})

@app.route('/retrieve_data', methods=['GET'])
def retrieve_data():
    data = {"key": "This is some example text"} 
    return jsonify(data)  # Return the data as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)  # Run the Flask server on port 
    






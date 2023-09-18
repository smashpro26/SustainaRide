import customtkinter
import requests
import time
import threading
import math

class PassengerPopup(customtkinter.CTkToplevel):
    def __init__(self,passenger_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = None
        self.passenger_data = passenger_data
        self.geometry("400x300")    
        self.driver_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindDriver)
        self.driver_refreshbtn.grid(row=1, column=0, sticky='nsew')     



        self.driverlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Driver_list')
        self.driverlist_scrollable.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.driverlist_scrollable.columnconfigure(0,weight=1)  

        self.FindDriver()

    def passenger_close_enough_to_driver(self,driver_lat,driver_lon,passenger_lat,passenger_lon,driver_pickup_range):
        # Radius of the Earth in miles
        earth_radius = 3958.8  # miles

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(driver_lat)
        lon1_rad = math.radians(driver_lon)
        lat2_rad = math.radians(passenger_lat)
        lon2_rad = math.radians(passenger_lon)

        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        
        #Check if passenger is in range
        if distance <= float(driver_pickup_range):
            return True
        else:
            return False
        


    def FindDriver(self):
        self.drivers = {}
        self.counter = 0
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        
        if self.drivers.status_code == 200:
            self.client_info = self.drivers.json()
            print(self.client_info)
            for self.counter, driver in enumerate(self.client_info):
                if self.passenger_close_enough_to_driver(
                    driver_lat=driver.get('driver_start_coordinates')[0],
                    driver_lon= driver.get('driver_start_coordinates')[1],
                    driver_pickup_range=driver.get('driver_pickup_range'),
                    passenger_lat=self.passenger_data['passenger_start_coordinates'][0],
                    passenger_lon=self.passenger_data['passenger_start_coordinates'][1]
                    ) == True:
                    
                    self.name = driver.get('name')
                    self.age = str(driver.get('age'))
                    self.num_plate = str(driver.get('numplate'))
                    print(self.name + " " + self.age + " " + self.num_plate)
                    driver_button = customtkinter.CTkButton(
                        master=self.driverlist_scrollable,
                        text="Name: " + self.name + " Age: " + self.age + " Numberplate: " + self.num_plate,
                        command=lambda count=self.counter: self.AcceptDriver(count)
                    )
                    driver_button.grid(row=self.counter, column=0, pady=(20, 0), padx=(20, 20), sticky='nsew')
        else:
            print(f"Failed to get driver information. Status code: {self.drivers.status_code}")
            print("Press the refresh button: ")

        print(self.drivers)

    def AcceptDriver(self,count):
        self.count = count
        print(self.passenger_data['name'])
        self.accepted_driver_name = self.client_info[count].get('name')

        self.data_to_send = {
            'driver_name': self.accepted_driver_name,
            'driver_age' : self.client_info[count].get('age'),
            'driver_numplate': self.client_info[count].get('numplate'),
            'passenger_name': self.passenger_data['name'],
            'passenger_age': self.passenger_data['age'],
            #'passenger_start': self.passenger_data['passenger_start'],
            'passenger_finaldest': self.passenger_data.get("passenger_finaldest"), 
            'passenger_index': count 
        }

        self.accepted_drivers = requests.post(f"http://surveyer.pythonanywhere.com/driver_accepted", json= self.data_to_send)
        print(self.accepted_drivers.content)

        self.toplevel_window = None
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = WaitForDriverResponse(self.passenger_data)
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    def get_count(self):
        return self.count
    
    
        
        

def PassengerPanel(passenger_data):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PassengerPopup(passenger_data)
    else:
        toplevel_window.focus()  # if window exists focus it

class WaitForDriverResponse(customtkinter.CTkToplevel):
    def __init__(self,passenger_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passenger_data = passenger_data
        self.geometry("500x200")
        self.title("Response from driver")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        self.status_label = customtkinter.CTkLabel(master= self, text="Waiting for response from driver")
        self.status_label.grid(row=0, column=0, sticky = "ew",pady=(20, 0), padx=(20, 20))

        self.task_thread = threading.Thread(target=self.look_for_driver_response)
        self.task_thread.start()

        
    def look_for_driver_response(self):
        self.driver_accepted = False
        while not self.driver_accepted:
            #print("got a new version of accepted passengers from the server")
            self.accepted_passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_accepted_passengers")
            
            if self.accepted_passengers.status_code == 200:
                self.accepted_passengers_json = self.accepted_passengers.json()
                print(self.accepted_passengers.content)
                for i, self.passenger in enumerate(self.accepted_passengers_json):
                    print(self.passenger_data['name'])
                    # Check if driver_name or driver_age is None and handle it
                    if self.passenger_data['name'] == self.passenger.get("passenger_name") :
                        print("This driver accepted your request")
                        self.status_label.configure(text= "Your driver has accepted. Name: " + self.passenger.get('driver_name') + " Age: " + self.passenger.get('driver_age') +" Numplate: " + self.passenger.get('driver_numplate'))
                        self.driver_accepted = True
            else:
                print(f"Failed to get accepted driver information. Status code: {self.accepted_passengers.status_code}")
            time.sleep(3)
        
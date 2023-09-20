#essential imports
import customtkinter
import requests
import threading
import time
from accept_passengers import accept_passenger
from Passengerpopup import PassengerPopup

#class for DriverPopup window
class DriverPopup(customtkinter.CTkToplevel):
    driver_accepted = False #initialise a class variable

    #Constructor for the DriverPopup window
    def __init__(self,driver_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_name = driver_name #sets driver's name
        self.geometry("400x300")    
        self.title ("Passengers Available")
        self.passenger_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindPassenger) #Refresh button to Find up-to-date passengers
        self.passenger_refreshbtn.grid(row=1, column=0, sticky='nsew') #aligns button


        self.passengerlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Passenger_list') #creates a scrollable frame
        self.passengerlist_scrollable.grid(row=0, column=0, sticky='nsew') #aligns the scrollabe frame
        self.columnconfigure(0, weight=1) #allows to expand when adjusting window size
        
        self.FindPassenger() #calls FindPassenger function to show passenger list their respective details
        
    #Function to fetch passenger data    
    def FindPassenger(self):
        self.passengers = {} #Initalises empty passenger dictionary
        self.counter = 0 #Initialises counter
        self.passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers") #get passenger data from server
        if self.passengers.status_code == 200: #checks whether passenger data is received successfully 
            self.client_info = self.passengers.json() #converts json to dictionary
            for passenger in self.client_info:
                self.name = passenger.get('name')
                self.age = str(passenger.get('age'))
                self.start = passenger.get('start')
                self.passenger_end_coordinates = passenger.get('passenger_end_coordinates')
                passenger = customtkinter.CTkLabel(master=self.passengerlist_scrollable,text="Name: " + self.name + " Age: " + self.age) #displats name and age
                passenger.grid(row = self.counter, column = 0,pady=(20, 0), padx=(20, 20), sticky='nsew')
                self.counter += 1 #iterates through all passengers to gather their specific ingo
            self.task_thread = threading.Thread(target=self.check_if_accepted) #calls check_if_accepted function to check if driver accepts request
            self.task_thread.start()
        else:
            print(f"Failed to get passenger information. Status code: {self.passengers.status_code}")
            print("Press the refresh button: ")
        
        

        print(self.passengers)
        self.driver_accepted = False


    #function to check if driver has accepted
    def check_if_accepted(self):
        while not (self.driver_accepted):
            print("got a new version of accepted drivers from the server")
            self.accepted_drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_accepted_drivers") #gets driver info
            self.passenger_data = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers") #gets passenger info
            self.passenger_data_json = self.passenger_data.json()
            

            
            if self.accepted_drivers.status_code == 200:
                self.accepted_drivers_json = self.accepted_drivers.json()
                print(self.accepted_drivers_json)
                print(self.passenger_data_json)
                for self.driver in self.accepted_drivers_json:
                    # Check if driver_name or driver_age is None and handle it
                    if self.driver_name == self.driver.get("driver_name") :
                        print("This driver got accepted")
                        self.passenger_info = {
                            'passenger_name': self.driver.get('passenger_name'),
                            'passenger_age': self.driver.get('passenger_age'),
                            'passenger_start':self.driver.get('passenger_start'),
                            'passenger_start_coordinates': self.passenger_data_json[PassengerPopup.get_count(self)-1].get('passenger_start_coordinates'), #gets passenger start and end coordinates
                            'passenger_end_coordinates' : self.passenger_data_json[PassengerPopup.get_count(self)-1].get('passenger_end_coordinates'),
                            'driver_name': self.driver.get('driver_name'),
                            'driver_age': self.driver.get('driver_age'),
                            'driver_numplate': self.driver.get('driver_numplate')
                        }
                        print(self.passenger_info['passenger_end_coordinates'])
                        accept_passenger(self.passenger_info) #passes passenger info through to function in accept_passenger.py
                        self.driver_accepted = True
            else:
                print(f"Failed to get accepted driver information. Status code: {self.accepted_drivers.status_code}")
            time.sleep(3)

        

'Driver popup window to find passengers'
def DriverPanel(driver_name):
    print(driver_name)
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = DriverPopup(driver_name)
    else:
        toplevel_window.focus()  # if window exists focus it
        


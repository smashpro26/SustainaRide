import customtkinter
import requests
import threading
import time
from accept_passengers import accept_passenger
from Passengerpopup import PassengerPopup


class DriverPopup(customtkinter.CTkToplevel):
    driver_accepted = False
    def __init__(self,driver_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_name = driver_name
        self.geometry("400x300")    
        self.passenger_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindPassenger)
        self.passenger_refreshbtn.grid(row=1, column=0, sticky='nsew')     


        self.passengerlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Passenger_list')
        self.passengerlist_scrollable.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        
        self.FindPassenger()
        
    def FindPassenger(self):
        self.passengers = {}
        self.counter = 0
        self.passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers")  
        if self.passengers.status_code == 200:
            self.client_info = self.passengers.json()
            for passenger in self.client_info:
                self.name = passenger.get('name')
                self.age = str(passenger.get('age'))
                self.start = passenger.get('start')
                self.finaldest = passenger.get('finaldest')
                passenger = customtkinter.CTkLabel(master=self.passengerlist_scrollable,text="Name: " + self.name + " Age: " + self.age)
                passenger.grid(row = self.counter, column = 0,pady=(20, 0), padx=(20, 20), sticky='nsew')
                self.counter += 1
            self.task_thread = threading.Thread(target=self.check_if_accepted)
            self.task_thread.start()
        else:
            print(f"Failed to get passenger information. Status code: {self.passengers.status_code}")
            print("Press the refresh button: ")
        
        
        #self.all_passengers = [self.all_passengers.append(passenger['name']) for passenger in self.passenger_list]
        #self.passenger_list.configure(text="\n".join(self.all_passengers))
        print(self.passengers)
        self.driver_accepted = False

    def check_if_accepted(self):
        while not (self.driver_accepted):
            print("got a new version of accepted drivers from the server")
            self.accepted_drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_accepted_drivers")
            self.passenger_data = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers")
            self.passenger_data_json = self.passenger_data.json()
            

            
            if self.accepted_drivers.status_code == 200:
                self.accepted_drivers_json = self.accepted_drivers.json()
                print(self.accepted_drivers_json)
                for self.driver in self.accepted_drivers_json:
                    
                    # Check if driver_name or driver_age is None and handle it
                    if self.driver_name == self.driver.get("driver_name") :
                        print("This driver got accepted")
                        self.passenger_info = {
                            'passenger_name': self.driver.get('passenger_name'),
                            'passenger_age': self.driver.get('passenger_age'),
                            'passenger_start':self.driver.get('passenger_start'),
                            'passenger_finaldest' : self.passenger_data_json[PassengerPopup.get_count()]['passenger_finaldest'],
                            'driver_name': self.driver.get('driver_name'),
                            'driver_age': self.driver.get('driver_age'),
                            'driver_numplate': self.driver.get('driver_numplate')
                        }
                        accept_passenger(self.passenger_info)
                        self.driver_accepted = True
            else:
                print(f"Failed to get accepted driver information. Status code: {self.accepted_drivers.status_code}")
            time.sleep(3)

        


def DriverPanel(driver_name):
    print(driver_name)
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = DriverPopup(driver_name)
    else:
        toplevel_window.focus()  # if window exists focus it


import customtkinter
import requests

class PassengerPopup(customtkinter.CTkToplevel):
    def __init__(self,passenger_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passenger_data = passenger_data
        self.geometry("400x300")    
        self.driver_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindDriver)
        self.driver_refreshbtn.grid(row=1, column=0, sticky='nsew')     



        self.driverlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Driver_list')
        self.driverlist_scrollable.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.driverlist_scrollable.columnconfigure(0,weight=1)  

        self.FindDriver()

    def FindDriver(self):
        self.drivers = {}
        self.counter = 0
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        
        if self.drivers.status_code == 200:
            self.client_info = self.drivers.json()
            print(self.client_info)
            for self.counter, driver in enumerate(self.client_info):
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

    def AcceptDriver(self, count):
        print(self.passenger_data['name'])
        self.accepted_driver_name = self.client_info[count].get('name')

        self.data_to_send = {
            'driver_name': self.accepted_driver_name,
            'passenger_name': self.passenger_data['name'],
            'passenger_age': self.passenger_data['age']
        }

        self.accepted_drivers = requests.post(f"http://surveyer.pythonanywhere.com/driver_accepted", json= self.data_to_send)
        print(self.accepted_drivers.content)
        
        

def PassengerPanel(passenger_data):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PassengerPopup(passenger_data)
    else:
        toplevel_window.focus()  # if window exists focus it
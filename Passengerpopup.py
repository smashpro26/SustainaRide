import customtkinter
import requests

class PassengerPopup(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")    
        self.driver_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindDriver)
        self.driver_refreshbtn.grid(row=1, column=0, sticky='nsew')     



        self.driverlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Driver_list')
        self.driverlist_scrollable.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.driverlist_scrollable.columnconfigure(0,weight=1)  


        #self.driver_list_label = customtkinter.CTkLabel(master = self.driverlist_scrollable, text="No one at the momenent",wraplength=380)
        #self.driver_list_label.grid(row=0, column=0, sticky='nsew')
        
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        if self.drivers.status_code == 200:
            self.client_info = self.drivers.json()
            print(self.client_info)
            self.counter = 0
            for driver in self.client_info:
                self.name = driver.get('name')
                self.age = str(driver.get('age'))
                self.num_plate = str(driver.get('numplate'))
                print(self.name + " " + self.age + " " + self.num_plate)
                driver = customtkinter.CTkLabel(master=self.driverlist_scrollable,text="Name: " + self.name + " Age: " + self.age + " Numberplate: " + self.num_plate)
                driver.grid(row = self.counter, column = 0,pady=(20, 0), padx=(20, 20), sticky='nsew')
                self.counter += 1
        

    def FindDriver(self):
        self.drivers = {}
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        if self.drivers.status_code == 200:
            print(self.client_info)
            for driver in self.client_info:
                self.name = driver.get('name')
                self.age = str(driver.get('age'))
                self.num_plate = str(driver.get('numplate'))
                print(self.name + " " + self.age + " " + self.num_plate)
                driver = customtkinter.CTkLabel(master=self.driverlist_scrollable,text="Name: " + self.name + " Age: " + self.age + " Numberplate: " + self.num_plate)
                driver.grid(row = self.counter, column = 0,pady=(20, 0), padx=(20, 20), sticky='nsew')
                self.counter += 1
        else:
            print(f"Failed to get driver information. Status code: {self.drivers.status_code}")
            print("Press the refresh button: ")

        print(self.drivers)
        

def PassengerPanel():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PassengerPopup()
    else:
        toplevel_window.focus()  # if window exists focus it
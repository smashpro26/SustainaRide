import customtkinter
import requests

class PassengerPopup(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")    
        self.driver_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindDriver)
        self.driver_refreshbtn.grid(row=1, column=0, sticky='nsew')     

        self.driver_list = customtkinter.CTkLabel(master = self, text="No one at the momenent")
        self.driver_list.grid(row=0, column=0, sticky='nsew')
        
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        if self.drivers.status_code == 200:
            client_info = self.drivers.json()
            print(client_info)
            self.driver_list.configure(text=self.drivers.content)
        
    def FindDriver(self):
        self.drivers = requests.get(f"http://surveyer.pythonanywhere.com/get_drivers")  
        if self.drivers.status_code == 200:
            client_info = self.drivers.json()
            print(client_info)
        else:
            print(f"Failed to get driver information. Status code: {self.drivers.status_code}")
            print("Press the refresh button: ")

        print(self.drivers)
        self.driver_list.configure(text=self.drivers.content)

def PassengerPanel():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PassengerPopup()
    else:
        toplevel_window.focus()  # if window exists focus it